#!/usr/bin/env python3
"""Generate a model from a complete protocol input, with per-run evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from datetime import datetime, timezone
from Config import CONFIG
from LLMInterface import LLMSession
from synthesize import synthesizeRules, synthesizeTemplateChecker
from property_templates import SUBTYPES


def persistant(project_dir, file_name, content):
    project = Path(project_dir).resolve()
    project.mkdir(parents=True, exist_ok=True)
    lib_link = project.parent / 'lib'
    library = Path(CONFIG.LIBDIR).resolve()
    if lib_link.exists() or lib_link.is_symlink():
        if lib_link.resolve() != library:
            raise ValueError(f'{lib_link} must resolve to the configured library {library}')
    else:
        lib_link.symlink_to(os.path.relpath(library, project.parent), target_is_directory=True)
    destination = project / file_name
    destination.write_text(content)
    return str(destination)


def pipeline_identity(text):
    """No credentials: identify the actual input, source, library, and model settings."""
    settings = CONFIG.model_dump(mode='json')
    for key in ('LOGFILE', 'CACHEFILE', 'OUTDIR', 'LOGDIR', 'CONFIG_FILE'):
        settings.pop(key, None)
    for provider in settings['PROVIDERS'].values():
        provider.pop('api_key', None)
    sources = {}
    for directory, pattern in ((Path(__file__).parent, '*.py'), (Path(CONFIG.LIBDIR), '*.maude')):
        for path in sorted(directory.glob(pattern)):
            sources[str(path.resolve())] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps([text, settings, sources], sort_keys=True).encode()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Generate a Maude model from the entire protocol or Mermaid diagram input.')
    parser.add_argument('protocol', help='path to diagram.md or a protocol description')
    parser.add_argument('mode', nargs='?', default='model', choices=['model', 'check'],
                        help='model (default): generate rules only; check: also build checker.maude from --property and model-check it')
    parser.add_argument('--property', choices=sorted(SUBTYPES), help='property template subtype for check mode')
    parser.add_argument('--attacker', help='attacker principal (default: userC; userA for CTRL-revoked)')
    parser.add_argument('--check-timeout', type=int, default=600, help='seconds for Maude model checking')
    parser.add_argument('--out', help='output directory (must be new unless --resume is supplied)')
    parser.add_argument('--resume', action='store_true', help='resume only a matching per-run cache')
    parser.add_argument('--rules-name', help='output filename; default is RULES_NAME from configuration')
    parser.add_argument('--maude', help='path to the Maude executable for validation')
    parser.add_argument('--validation-timeout', type=int, default=30)
    parser.add_argument('--skip-validation', action='store_true', help='generate only; record validation as not_run')
    args = parser.parse_args(argv)
    if args.mode == 'check' and not args.property:
        parser.error(f'check mode requires --property, one of {sorted(SUBTYPES)}')
    if (args.property or args.attacker) and args.mode != 'check':
        parser.error('--property/--attacker are only supported in check mode')
    if args.validation_timeout <= 0:
        parser.error('--validation-timeout must be positive')
    source = Path(args.protocol).resolve()
    text = source.read_text()
    if not text.strip():
        parser.error('protocol input is empty')
    name = source.parent.name if source.name == 'diagram.md' else source.stem
    run_name = f'{name}-{time.time_ns()}'
    project = Path(args.out or Path(CONFIG.OUTDIR) / run_name).resolve()
    if project.exists() and any(project.iterdir()) and not args.resume:
        parser.error('output directory is not empty; use a new --out directory or --resume')
    filename = args.rules_name or CONFIG.RULES_NAME
    if Path(filename).name != filename or not filename.endswith('.maude'):
        parser.error('--rules-name must be a .maude filename, not a path')
    if args.mode == 'check' and filename != 'rules.maude':
        parser.error('legacy checker loads rules.maude; use --rules-name rules.maude')
    project.mkdir(parents=True, exist_ok=True)
    CONFIG.LOGFILE = str(project / 'llm.log')
    CONFIG.CACHEFILE = str(project / '.cache.json')
    CONFIG.DEBUG = False  # Batch runs must never enter an interactive prompt/debugger.
    identity = pipeline_identity(text + (f'\n{args.property}:{args.attacker}' if args.property else ''))
    llm = LLMSession(context_id=identity)
    manifest_path = project / 'run.json'
    manifest = {'input': str(source), 'input_sha256': hashlib.sha256(text.encode()).hexdigest(),
                'pipeline_id': identity, 'mode': args.mode, 'started_at': datetime.now(timezone.utc).isoformat(),
                'status': 'running', 'validation': {'status': 'not_run'},
                'model_file': filename, 'source_kind': 'diagram' if 'sequenceDiagram' in text else 'text'}
    start = time.monotonic()
    try:
        if args.resume and llm.hasCache():
            llm.loadCache()
        elif args.resume:
            raise ValueError('No cache exists to resume in this output directory.')
        (project / 'input.md').write_text(text)
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
        # The diagram is already structured, so every agent reads the whole input; there is no split stage.
        # synthesizeRules labels the diagram blocks and returns a rule-to-block trace for diagram input.
        llm.source_context = text
        rules, state_template, events, trace = synthesizeRules(llm, text, args.property)
        model_path = persistant(project, filename, rules)
        if trace is not None:
            (project / 'trace.json').write_text(json.dumps(trace, indent=2) + '\n')
            manifest['trace'] = {'blocks': len(trace['blocks']), 'coverage_issues': trace['coverage_issues']}
        manifest['model_sha256'] = hashlib.sha256(rules.encode()).hexdigest()
        manifest['status'] = 'generated'
        if not args.skip_validation:
            from model_validation import validate_model
            validation = validate_model(model_path, maude_binary=args.maude, timeout=args.validation_timeout)
            for key in ('stdout', 'stderr'):
                (project / f'maude.{key}.txt').write_text(validation.get(key, ''))
            manifest['validation'] = {k: v for k, v in validation.items() if k not in ('stdout', 'stderr')}
            manifest['status'] = 'validated' if validation['status'] == 'valid' else 'validation_failed'
        if args.mode == 'check' and manifest['status'] != 'validation_failed':
            from model_validation import run_checker
            checker, props = synthesizeTemplateChecker(llm, args.property, rules, state_template, args.attacker)
            checker_path = persistant(project, CONFIG.CHECKER_NAME, checker)
            result = run_checker(checker_path, props, maude_binary=args.maude, timeout=args.check_timeout)
            (project / 'maude.check.stdout.txt').write_text(result['stdout'])
            (project / 'counterexample.txt').write_text('\n'.join(result['events']) + '\n')
            manifest['check'] = {'property': args.property, 'verdict': result['verdict'],
                                 'events': len(result['events']), 'at_init': result['at_init'],
                                 'true_at_init': [p for p, v in result['at_init'].items() if v],
                                 'errors': result['errors']}
            print(f'[+] Check {args.property}: {result["verdict"]} ({len(result["events"])} events)')
            if result['verdict'] not in ('counterexample', 'holds'):
                return 3
        print(f'[+] Model written: {model_path}; status: {manifest["status"]}')
        return 0 if manifest['status'] != 'validation_failed' else 2
    except Exception as exc:
        manifest['status'] = 'failed'
        manifest['error'] = f'{type(exc).__name__}: {exc}'
        print(f'[-] {manifest["error"]}', file=sys.stderr)
        return 1
    finally:
        manifest['elapsed_seconds'] = round(time.monotonic() - start, 3)
        manifest['tokens_this_run'] = llm.tokens
        manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
        (project / 'stages.json').write_text(json.dumps(llm.stage_records, indent=2) + '\n')


if __name__ == '__main__':
    sys.exit(main())

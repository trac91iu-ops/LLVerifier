#!/usr/bin/env python3
"""Repeat the full end-to-end run with a frozen configuration, for Pass@1 and k/n success.

Each repeat is an independent pipeline sample: run_all_e2e.py writes into a new directory, so the
per-run LLM cache (OUT/<protocol>/.cache.json) starts empty. Before the first repeat, a manifest
records the SHA-256 of every input diagram and of the code, prompts, configs and libraries, and every
later repeat refuses to start if any of them changed.
The configuration is configs/config.yaml, or the file named by LLVERIFIER_CONFIG (src/Config.py); it is recorded in
the manifest, and a later repeat with another configuration refuses to start.
Usage: python scripts/run_repeats.py EVAL_DIR FIRST LAST [PROTOCOL ...] [--jobs N]
       PROTOCOL names the protocols to run (default: every IoT protocol, see run_all_e2e.py); the manifest records them.
       e.g. python scripts/run_repeats.py sequence_diagram/output/a2a-astra-20261105 1 5 A2A
       e.g. python scripts/run_repeats.py sequence_diagram/output/eval-v1-20261102 2 5 --jobs 8
            LLVERIFIER_CONFIG=config-norepair.yaml python scripts/run_repeats.py sequence_diagram/output/ablation-norepair-20261104 1 5
"""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ['src/*.py', 'configs/*.yaml', 'lib/*.maude', 'scripts/run_all_e2e.py', 'scripts/validate_property_templates.py',
          'sequence_diagram/input/*/diagram.md']


def fingerprint():
    files = sorted(p for pattern in FROZEN for p in ROOT.glob(pattern) if p.is_file())
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def main(argv):
    jobs = 8
    if '--jobs' in argv:
        i = argv.index('--jobs'); jobs = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    out, first, last, selected = Path(argv[0]).resolve(), int(argv[1]), int(argv[2]), argv[3:]
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / 'manifest.json'
    current = fingerprint()
    config = os.environ.get('LLVERIFIER_CONFIG', 'config.yaml')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest.get('config', 'config.yaml') != config:
            sys.exit(f'{out} was run with {manifest.get("config", "config.yaml")}, not {config}')
        if manifest.get('protocols', []) != selected:
            sys.exit(f'{out} was run with protocols {manifest.get("protocols", [])}, not {selected}')
        changed = sorted(k for k in set(manifest['files']) | set(current) if manifest['files'].get(k) != current.get(k))
        if changed:
            sys.exit(f'frozen files changed since {manifest["created_at"]}: {changed}')
    else:
        manifest = {'created_at': datetime.now(timezone.utc).isoformat(), 'config': config, 'protocols': selected,
                    'files': current, 'runs': {}}
    for n in range(first, last + 1):
        target = out / f'run{n}'
        if target.exists():
            sys.exit(f'{target} exists; repeats are never overwritten')
        started = datetime.now(timezone.utc).isoformat()
        code = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/run_all_e2e.py'), str(target), *selected, '--jobs', str(jobs)]).returncode
        manifest['runs'][f'run{n}'] = {'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(), 'exit': code}
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
        if fingerprint() != current:
            sys.exit(f'frozen files changed during run{n}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Run diagram -> rules.maude -> checker.maude -> counterexample for every IoT protocol (A2A only when named).

Each protocol uses the property subtype of its golden checker. Per protocol, a comparison.md
puts the golden counterexample (golden rules + golden checker) next to the generated one.
Usage: python scripts/run_all_e2e.py OUT_DIR [protocol ...] [--jobs N]
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_property_templates as V

INPUT = ROOT / 'sequence_diagram/input'
GOLDEN_NAME = {'philips': 'Philips'}


def protocols():
    return sorted(d.name for d in INPUT.iterdir() if (d / 'diagram.md').exists() and d.name != 'A2A')


def run(protocol, out, binary, lib):
    golden = GOLDEN_NAME.get(protocol, protocol)
    subtype, _, attacker = V.MAPPING[golden]
    target = out / protocol
    with open(out / f'{protocol}.console.txt', 'w') as console:
        code = subprocess.run([sys.executable, '-B', str(ROOT / 'src/main.py'), str(INPUT / protocol / 'diagram.md'),
                               'check', '--property', subtype, '--attacker', attacker, '--out', str(target)],
                              stdout=console, stderr=subprocess.STDOUT).returncode
    manifest = json.loads((target / 'run.json').read_text()) if (target / 'run.json').exists() else {}
    check = manifest.get('check', {})
    trace = json.loads((target / 'trace.json').read_text()) if (target / 'trace.json').exists() else {}
    generated = [e for e in (target / 'counterexample.txt').read_text().splitlines() if e.strip()] \
        if (target / 'counterexample.txt').exists() else []
    gold_verdict, gold_events = V.check(binary, lib, V.GOLD / golden)
    row = dict(protocol=protocol, subtype=subtype, attacker=attacker, exit=code, status=manifest.get('status'),
               error=manifest.get('error'), verdict=check.get('verdict'), events=len(generated),
               golden_verdict=gold_verdict, golden_events=len(gold_events), true_at_init=check.get('true_at_init'),
               coverage_issues=trace.get('coverage_issues'), calls=None)
    slots = []
    if (target / 'checker.maude').exists():
        slots = [l for l in (target / 'checker.maude').read_text().splitlines() if l.startswith(('eq E @ S', 'ceq E @ S |= attackerActs'))]
    lines = [f'# {protocol}', '', f'- input: `sequence_diagram/input/{protocol}/diagram.md`',
             f'- output: `{target.relative_to(ROOT)}/`', f'- property: {subtype} (attacker {attacker})',
             f"- status: {row['status']}; verdict: {row['verdict']} ({row['events']} events); golden: {gold_verdict} ({len(gold_events)} events)",
             f"- slots false at init expected; true at init: {row['true_at_init']}", f"- coverage issues: {row['coverage_issues']}"]
    if row['error']:
        lines.append(f"- error: {row['error']}")
    lines += ['', '## Generated slots', '```', *slots, '```', '', '## Counterexamples', '',
              '| # | golden | generated |', '|---|---|---|']
    for i in range(max(len(gold_events), len(generated))):
        g = gold_events[i] if i < len(gold_events) else ''
        n = generated[i] if i < len(generated) else ''
        lines.append(f'| {i + 1} | `{g}` | `{n}` |' if g or n else '')
    target.mkdir(parents=True, exist_ok=True)
    (target / 'comparison.md').write_text('\n'.join(lines) + '\n')
    return row


def main(argv):
    jobs = 8
    if '--jobs' in argv:
        i = argv.index('--jobs'); jobs = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    out = Path(argv[0]).resolve(); out.mkdir(parents=True, exist_ok=True)
    selected = argv[1:] or protocols()
    binary, lib = V.maudeBinary()
    with ThreadPoolExecutor(jobs) as ex:
        rows = list(ex.map(lambda p: run(p, out, binary, lib), selected))
    (out / 'summary.json').write_text(json.dumps(rows, indent=2) + '\n')
    for r in rows:
        print(f"{r['protocol']:16} {r['subtype']:13} {str(r['status']):18} {str(r['verdict']):15} {r['events']:3} events | "
              f"golden {r['golden_verdict']:14} {r['golden_events']:3} | init-true {r['true_at_init']} | "
              f"cov {len(r['coverage_issues'] or [])} | {(r['error'] or '')[:90]}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Collect, per protocol, the input diagram, the golden model and the generated models of every run into one folder,
for filling the semantic-fidelity columns by hand.

OUT_DIR/<protocol>/ gets diagram.md, gold.rules.maude, gold.checker.maude and runN.rules.maude / runN.checker.maude
(copied as they are), plus all.txt with everything in one file. Runs whose generated model is byte-identical to an
earlier run are marked in all.txt and index.md, so each distinct model only needs to be read once.
OUT_DIR/index.md lists the protocols, the verdict of each run and the distinct models.
Usage: python scripts/collect_fidelity_inputs.py OUT_DIR RUN_DIR [RUN_DIR ...]
"""
import hashlib, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'sequence_diagram/input'
GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def section(title, path):
    body = path.read_text() if path.exists() else '(missing)\n'
    return f'{"=" * 100}\n=== {title}\n{"=" * 100}\n{body.rstrip()}\n\n'


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    out = Path(argv[0]).resolve()
    runs = [Path(d).resolve() for d in argv[1:]]
    if out.exists():
        sys.exit(f'{out} exists; choose a new directory')
    summaries = [{r['protocol']: r for r in json.loads((d / 'summary.json').read_text())} for d in runs]
    index = ['# Semantic-fidelity inputs', '', 'Runs:', '']
    index += [f'- run{i}: `{d.relative_to(ROOT) if d.is_relative_to(ROOT) else d}`' for i, d in enumerate(runs, 1)]
    index += ['', '| Protocol | Gold | ' + ' | '.join(f'run{i}' for i in range(1, len(runs) + 1)) + ' | Distinct models |',
              '|---|---|' + '---|' * len(runs) + '---|']
    for name in sorted(summaries[0], key=str.lower):
        dest = out / name
        dest.mkdir(parents=True)
        gold = GOLD / GOLDEN_NAME.get(name, name)
        shutil.copyfile(INPUT / name / 'diagram.md', dest / 'diagram.md')
        shutil.copyfile(gold / 'rules.maude', dest / 'gold.rules.maude')
        shutil.copyfile(gold / 'checker.maude', dest / 'gold.checker.maude')
        text = [section(f'{name} input diagram', INPUT / name / 'diagram.md'),
                section(f'{name} golden rules', gold / 'rules.maude'),
                section(f'{name} golden checker', gold / 'checker.maude')]
        seen, cells = {}, []
        for i, (d, summary) in enumerate(zip(runs, summaries), 1):
            row = summary[name]
            rules = d / name / 'rules.maude'
            for kind in ('rules', 'checker'):
                if (d / name / f'{kind}.maude').exists():
                    shutil.copyfile(d / name / f'{kind}.maude', dest / f'run{i}.{kind}.maude')
            key = (sha(rules), sha(d / name / 'checker.maude'))
            verdict = f"{row['status']}, {row['verdict']}"
            if key in seen:
                cells.append(f'{verdict} (= run{seen[key]})')
                text.append(f'{"=" * 100}\n=== run{i} ({verdict}) is identical to run{seen[key]}\n{"=" * 100}\n\n')
                continue
            seen[key] = i
            cells.append(verdict)
            text += [section(f'run{i} generated rules ({verdict})', rules),
                     section(f'run{i} generated checker', d / name / 'checker.maude')]
        (dest / 'all.txt').write_text(''.join(text))
        index.append(f"| {name} | {summaries[0][name]['golden_verdict']} | " + ' | '.join(cells) + f' | {len(seen)} |')
    (out / 'index.md').write_text('\n'.join(index) + '\n')
    print((out / 'index.md').read_text())
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

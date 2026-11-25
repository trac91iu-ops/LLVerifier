#!/usr/bin/env python3
"""Score Trace Equiv. from the manual verdicts of the review page (evaluation/review/index.html).

The page stores one verdict per distinct generated model (present, absent or unsure) in the artifact database,
collection 'verdicts'. Export them with the ArtifactData tool (action list, collection verdicts, out_dir
evaluation/results/trace_equiv_manual/export), or paste the page's "Copy verdicts as JSON" into a file.
A run scores 1 if its model is judged present, 0 if absent or if its model did not load. Per protocol,
Trace Equiv. = runs scored 1 / runs, in percent; the All row averages the protocols.
A model with no verdict, or with unsure, stops the scoring unless --partial is given (then only the progress is printed).
Writes per_run.csv, per_protocol.csv and table.md to OUT_DIR (default evaluation/results/trace_equiv_manual).
Usage: python evaluation/trace_equiv_manual.py [--partial] [--data FILE] VERDICTS [OUT_DIR]
       VERDICTS is a JSON file (a list of verdicts) or a directory of one JSON file per verdict.
       --data names the review data (default evaluation/results/trace_equiv_review/data.json), e.g.
       evaluation/results/trace_equiv_review_llm_luna6/data.json for the GPT-6 Luna page.
"""
import argparse, csv, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / 'results/trace_equiv_review/data.json'
DISPLAY = {'philips': 'Philips Hue'}


def load_verdicts(path):
    path = Path(path)
    docs = [json.loads(f.read_text()) for f in sorted(path.rglob('*.json'))] if path.is_dir() else json.loads(path.read_text())
    docs = [d.get('data', d) for d in docs]  # ArtifactData files may wrap the body
    return {(d['protocol'], d['model']): d for d in docs if d.get('verdict')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('verdicts')
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/trace_equiv_manual'))
    ap.add_argument('--partial', action='store_true')
    ap.add_argument('--data', default=str(DATA))
    a = ap.parse_args()
    data = json.loads(Path(a.data).read_text())
    verdicts = load_verdicts(a.verdicts)
    rows, missing = [], []
    for p in data['protocols']:
        for m in p['models']:
            v = verdicts.get((p['protocol'], m['id']), {}).get('verdict')
            if v not in ('present', 'absent'):
                missing.append(f"{p['protocol']} {m['id']} ({v or 'no verdict'})")
        for r in p['runs']:
            v = verdicts.get((p['protocol'], r.get('model')), {}) if r['status'] == 'validated' else {}
            rows.append(dict(protocol=p['protocol'], run=r['run'], model=r.get('model', ''),
                             verdict=v.get('verdict', '') if r['status'] == 'validated' else 'model did not load',
                             note=' '.join(v.get('note', '').split())))
    models = sum(len(p['models']) for p in data['protocols'])
    print(f'{models - len(missing)}/{models} models decided')
    if missing:
        print('undecided: ' + '; '.join(missing))
        if not a.partial:
            return 1
        return 0
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    per = []
    for p in data['protocols']:
        sel = [r for r in rows if r['protocol'] == p['protocol']]
        k = sum(r['verdict'] == 'present' for r in sel)
        per.append(dict(protocol=p['protocol'], runs=len(sel), present=k, trace_equiv=round(100 * k / len(sel), 1)))
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    overall = round(statistics.mean(p['trace_equiv'] for p in per), 1)
    table = ['| Protocol | Gold attack present (manual) | Trace Equiv. (%) |', '|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['present']}/{p['runs']} | {p['trace_equiv']} |" for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | {sum(p['present'] for p in per)}/"
                 f"{sum(p['runs'] for p in per)} | {overall} |")
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    print('\n'.join(table))
    return 0


if __name__ == '__main__':
    sys.exit(main())

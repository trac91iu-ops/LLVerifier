#!/usr/bin/env python3
"""State Trans. accuracy and recall: compare the state rules of every generated model with those of the gold model.

For each run listed in evaluation/runs.txt and each protocol, the generated rules.maude is renamed into the gold
vocabulary with its mapping (evaluation/mappings/<protocol>/<sha256[:12]>.json) and compared rule by rule (rules.py).
  accuracy = generated state rules that match some gold rule / generated state rules
  recall   = gold state rules matched by some generated rule / gold state rules
at two levels: effect (same trigger, updates and emitted messages) and exact (effect plus guards, see rules.py).
Per protocol the five runs are averaged; the All row averages the protocols. Runs whose model failed to load are
scored too (the rules are text) and flagged; the summary also gives the aggregates over loaded runs only.
Writes per_run.csv, per_protocol.csv, summary.json, table.md and details/<protocol>.md (every rule pairing) to OUT_DIR.
Usage: python evaluation/state_trans.py [OUT_DIR]   (default evaluation/results/state_trans)
"""
import csv, hashlib, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import rules as R  # noqa: E402

GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}
DISPLAY = {'philips': 'Philips Hue'}
CATEGORIES = ('actions', 'attributes', 'principals', 'constants')
LEVELS = ('effect', 'exact')


def pct(k, n):
    return round(100 * k / n, 1) if n else None


def score(gold, gen, mapping, values, actions):
    G = [R.canon(r, gold, {}) for r in gold.rules]
    C = [R.canon(r, gen, mapping, values, actions) for r in gen.rules]
    res = [[R.compare(c, g) for g in G] for c in C]
    out = dict(gold_rules=len(G), gen_rules=len(C))
    for lvl in LEVELS:
        prec = [any(x[0] if lvl == 'effect' else x[1] for x in row) for row in res]
        rec = [any((res[i][j][0] if lvl == 'effect' else res[i][j][2]) for i in range(len(C))) for j in range(len(G))]
        out[f'{lvl}_matched_gen'], out[f'{lvl}_matched_gold'] = sum(prec), sum(rec)
        out[f'{lvl}_acc'], out[f'{lvl}_rec'] = pct(sum(prec), len(C)), pct(sum(rec), len(G))
    return out, res


def details(gold, gen, res):
    lines = ['| gen \\ gold | ' + ' | '.join(f'g{j + 1}' for j in range(len(gold.rules))) + ' |',
             '|---|' + '---|' * len(gold.rules)]
    mark = lambda x: 'exact' if x[1] and x[2] else 'exact (gen narrower)' if x[1] else 'exact (gen wider)' if x[2] else 'effect' if x[0] else ''
    for i, row in enumerate(res):
        lines.append(f'| r{i + 1} | ' + ' | '.join(mark(x) for x in row) + ' |')
    lines += ['', 'Gold rules:', ''] + [f'- g{j + 1}: `{r.text}`' for j, r in enumerate(gold.rules)]
    lines += ['', 'Generated rules (names as generated):', ''] + [f'- r{i + 1}: `{r.text}`' for i, r in enumerate(gen.rules)]
    return lines


def main(argv):
    out = Path(argv[0]).resolve() if argv else HERE / 'results/state_trans'
    runs = [l.split(None, 1) for l in (HERE / 'runs.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
    rows, unreviewed, notes = [], set(), {}
    for name, d in runs:
        d = ROOT / d.strip()
        summary = {r['protocol']: r for r in json.loads((d / 'summary.json').read_text())}
        for protocol in sorted(summary, key=str.lower):
            f = d / protocol / 'rules.maude'
            sha = hashlib.sha256(f.read_bytes()).hexdigest()
            mfile = HERE / 'mappings' / protocol / f'{sha[:12]}.json'
            if not mfile.exists():
                sys.exit(f'no mapping {mfile.relative_to(ROOT)}; run evaluation/propose_mappings.py first')
            m = json.loads(mfile.read_text())
            if m['mapping'] is None:
                sys.exit(f'{mfile.relative_to(ROOT)} has no valid mapping')
            if not m['reviewed']:
                unreviewed.add(str(mfile.relative_to(ROOT)))
            flat = {k: v for c in CATEGORIES if c != 'actions' for k, v in m['mapping'][c].items() if v is not None}
            actions = {k: v for k, v in m['mapping']['actions'].items() if v is not None}
            gold = R.load_model(GOLD / GOLDEN_NAME.get(protocol, protocol) / 'rules.maude')
            gen = R.load_model(f)
            values = [(v['attribute'], v['generated'], v['gold']) for v in m['mapping'].get('values', [])]
            s, res = score(gold, gen, flat, values, actions)
            rows.append(dict(protocol=protocol, run=name, loaded=summary[protocol]['status'] == 'validated',
                             mapping=mfile.name, reviewed=m['reviewed'], **s))
            key = (protocol, sha)
            if key not in notes:
                notes[key] = [f'## {mfile.name} ({", ".join(m["runs"])})', '', f'effect acc {s["effect_acc"]} rec {s["effect_rec"]}; '
                              f'exact acc {s["exact_acc"]} rec {s["exact_rec"]}', ''] + details(gold, gen, res) + ['']
    out.mkdir(parents=True, exist_ok=True)
    (out / 'details').mkdir(exist_ok=True)
    for protocol in {p for p, _ in notes}:
        body = [f'# {protocol}: state rules, generated vs. gold', '',
                'Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. '
                'exact: also the same guards. gen narrower: the generated rule requires more (precise but does not '
                'recall g). gen wider: the generated rule requires less (recalls g but is not precise).', '']
        for (p, _), lines in notes.items():
            if p == protocol:
                body += lines
        (out / 'details' / f'{protocol}.md').write_text('\n'.join(body))
    cols = list(rows[0])
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, cols); w.writeheader(); w.writerows(rows)

    def agg(sel):
        per = []
        for protocol in sorted({r['protocol'] for r in sel}, key=str.lower):
            rs = [r for r in sel if r['protocol'] == protocol]
            per.append(dict(protocol=protocol, runs=len(rs), gold_rules=rs[0]['gold_rules'],
                            gen_rules=statistics.median(r['gen_rules'] for r in rs),
                            **{f'{l}_{k}': round(statistics.mean(r[f'{l}_{k}'] for r in rs), 1) for l in LEVELS for k in ('acc', 'rec')}))
        overall = {f'{l}_{k}': round(statistics.mean(p[f'{l}_{k}'] for p in per), 1) for l in LEVELS for k in ('acc', 'rec')}
        micro = {f'{l}_{k}': pct(sum(r[f'{l}_matched_{"gen" if k == "acc" else "gold"}'] for r in sel),
                                 sum(r['gen_rules' if k == 'acc' else 'gold_rules'] for r in sel)) for l in LEVELS for k in ('acc', 'rec')}
        return per, overall, micro

    per, overall, micro = agg(rows)
    _, overall_loaded, micro_loaded = agg([r for r in rows if r['loaded']])
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    table = ['| Protocol | Gold rules | Gen rules (median) | Effect Acc. | Effect Rec. | Exact Acc. | Exact Rec. |',
             '|---|---|---|---|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['gold_rules']} | {p['gen_rules']} | {p['effect_acc']} | "
              f"{p['effect_rec']} | {p['exact_acc']} | {p['exact_rec']} |" for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | | | {overall['effect_acc']} | {overall['effect_rec']} | "
                 f"{overall['exact_acc']} | {overall['exact_rec']} |")
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    (out / 'summary.json').write_text(json.dumps(dict(
        runs=dict(runs), mean_of_protocols=overall, pooled_rules=micro, mean_of_protocols_loaded_runs_only=overall_loaded,
        pooled_rules_loaded_runs_only=micro_loaded, unreviewed_mappings=len(unreviewed)), indent=2) + '\n')
    print('\n'.join(table))
    print(f'\npooled over all rules: {micro}')
    print(f'loaded runs only: mean of protocols {overall_loaded}, pooled {micro_loaded}')
    if unreviewed:
        print(f'\nWARNING: {len(unreviewed)} mappings not yet reviewed by a human (set "reviewed": true after checking).')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

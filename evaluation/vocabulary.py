#!/usr/bin/env python3
"""Principals and Attributes accuracy and recall: compare the vocabulary of every generated model with the gold model.

Names are aligned with the reviewed mapping of each model (evaluation/mappings/<protocol>/<sha256[:12]>.json).
  Principals  the principal constants of the model (userA, deviceB, cloudA, ...), from the initial state and the state
              rules. The system object (fresh counter, clock) is modelling machinery, not a principal, and is left out.
  Attributes  the attributes of each principal, as owner path plus name, e.g. deviceB.'key' or cloudA.User.'members'.
              Users share one schema, so every user constant and User variable becomes User. A Device/Cloud variable
              becomes the model's only device/cloud; paths through other variables are skipped. Attributes come from
              the initial state and the state rules. Fields inside a set value (a ticket record) are values, not
              attributes. The system object is left out.
  accuracy = generated elements whose mapped name is a gold element / generated elements
  recall   = gold elements that some generated element maps to / gold elements
Per protocol the five runs are averaged; the All row averages the protocols. Runs whose model failed to load are
scored too and flagged; summary.json also gives the aggregates over loaded runs only.
Writes per_run.csv, per_protocol.csv, summary.json, table.md and details/<protocol>.md to OUT_DIR.
Usage: python evaluation/vocabulary.py [OUT_DIR]   (default evaluation/results/vocabulary)
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
SYSTEM_OBJECT = 'system'
KINDS = ('principals', 'attributes')


def pct(k, n):
    return round(100 * k / n, 1) if n else None


def vocabulary(model):
    """(principals, attributes) of a model, in its own names."""
    pm, am = {}, {}
    inv = R.inventory(model)
    principals = {pm.get(p, p) for p in inv['principals']} - {SYSTEM_OBJECT}
    only = {}
    for sort, prefix in (('Device', 'device'), ('Cloud', 'cloud')):
        consts = R.device_constants(model, prefix)
        if len(consts) == 1:
            only[sort] = pm.get(consts[0], consts[0])

    def owner(t):
        sort = model.variables.get(t)
        if sort == 'User':
            return 'User'
        if sort is not None:
            return only.get(sort)
        t = pm.get(t, t)
        return 'User' if t.startswith('user') else t

    paths = set()
    init_attrs = R.parse_soup(model.init.split('@', 1)[1].rstrip(' .'))[0] if '@' in model.init else {}
    for path in [*init_attrs, *(p for r in model.rules for d in (r.pre, r.post) for p in d)]:
        *owners, name = path
        owners = [owner(t) for t in owners]
        if None in owners or owners[0] == SYSTEM_OBJECT or not R.QID.match(name):
            continue
        paths.add('.'.join(owners) + '.' + am.get(name, name))
    return principals, paths


def main(argv):
    out = Path(argv[0]).resolve() if argv else HERE / 'results/vocabulary'
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
            pmap = {k: v for k, v in m['mapping']['principals'].items() if v is not None}
            amap = {k: v for k, v in m['mapping']['attributes'].items() if v is not None}
            gold = vocabulary(R.load_model(GOLD / GOLDEN_NAME.get(protocol, protocol) / 'rules.maude'))
            gen_raw = vocabulary(R.load_model(f))
            row = dict(protocol=protocol, run=name, loaded=summary[protocol]['status'] == 'validated',
                       mapping=mfile.name, reviewed=m['reviewed'])
            detail = []
            for kind, g, raw in zip(KINDS, gold, gen_raw):
                # each generated element on its own, so two that map to one gold element both count
                raw_to_mapped = {x: vocabulary_one(kind, x, pmap, amap) for x in raw}
                correct = [x for x, y in raw_to_mapped.items() if y in g]
                covered = g & set(raw_to_mapped.values())
                row.update({f'gold_{kind}': len(g), f'gen_{kind}': len(raw), f'{kind}_correct': len(correct),
                            f'{kind}_covered': len(covered), f'{kind}_acc': pct(len(correct), len(raw)),
                            f'{kind}_rec': pct(len(covered), len(g))})
                detail += [f'**{kind}**: acc {row[f"{kind}_acc"]} ({len(correct)}/{len(raw)}), '
                           f'rec {row[f"{kind}_rec"]} ({len(covered)}/{len(g)})', '',
                           '- generated, not in gold: ' + (', '.join(f'`{x}` → `{raw_to_mapped[x]}`'
                                                                    for x in sorted(set(raw) - set(correct))) or 'none'),
                           '- gold, not generated: ' + (', '.join(f'`{x}`' for x in sorted(g - covered)) or 'none'), '']
            rows.append(row)
            if (protocol, sha) not in notes:
                notes[(protocol, sha)] = [f'## {mfile.name} ({", ".join(m["runs"])})', ''] + detail
    out.mkdir(parents=True, exist_ok=True)
    (out / 'details').mkdir(exist_ok=True)
    for protocol in sorted({p for p, _ in notes}):
        body = [f'# {protocol}: principals and attributes, generated vs. gold', '',
                'Attributes are written owner path + name; User stands for every user. Generated names are shown '
                'as generated and, after the arrow, as mapped.', '']
        body += [l for (p, _), lines in notes.items() if p == protocol for l in lines]
        (out / 'details' / f'{protocol}.md').write_text('\n'.join(body) + '\n')
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    metrics = [f'{k}_{s}' for k in KINDS for s in ('acc', 'rec')]

    def agg(sel):
        per = []
        for protocol in sorted({r['protocol'] for r in sel}, key=str.lower):
            rs = [r for r in sel if r['protocol'] == protocol]
            per.append(dict(protocol=protocol, runs=len(rs), gold_principals=rs[0]['gold_principals'],
                            gold_attributes=rs[0]['gold_attributes'],
                            **{k: round(statistics.mean(r[k] for r in rs), 1) for k in metrics}))
        overall = {k: round(statistics.mean(p[k] for p in per), 1) for k in metrics}
        pooled = {f'{k}_{s}': pct(sum(r[f'{k}_{"correct" if s == "acc" else "covered"}'] for r in sel),
                                  sum(r[f'{"gen" if s == "acc" else "gold"}_{k}'] for r in sel))
                  for k in KINDS for s in ('acc', 'rec')}
        return per, overall, pooled

    per, overall, pooled = agg(rows)
    _, overall_loaded, pooled_loaded = agg([r for r in rows if r['loaded']])
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    table = ['| Protocol | Gold principals | Gold attributes | Principals Acc. | Principals Rec. | Attributes Acc. | '
             'Attributes Rec. |', '|---|---|---|---|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['gold_principals']} | {p['gold_attributes']} | "
              + ' | '.join(str(p[k]) for k in metrics) + ' |' for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | | | " + ' | '.join(str(overall[k]) for k in metrics) + ' |')
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    (out / 'summary.json').write_text(json.dumps(dict(
        runs=dict(runs), mean_of_protocols=overall, pooled=pooled, mean_of_protocols_loaded_runs_only=overall_loaded,
        pooled_loaded_runs_only=pooled_loaded, unreviewed_mappings=len(unreviewed)), indent=2) + '\n')
    print('\n'.join(table))
    print(f'\npooled: {pooled}\nloaded runs only: mean of protocols {overall_loaded}, pooled {pooled_loaded}')
    if unreviewed:
        print(f'\nWARNING: {len(unreviewed)} mappings not yet reviewed by a human (set "reviewed": true after checking).')
    return 0


def vocabulary_one(kind, x, pmap, amap):
    """The mapped form of one generated principal or attribute path (as returned by vocabulary without a mapping)."""
    if kind == 'principals':
        return pmap.get(x, x)
    *owners, name = x.split('.')
    owners = ['User' if pmap.get(o, o).startswith('user') else pmap.get(o, o) for o in owners]
    return '.'.join(owners) + '.' + amap.get(name, name)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

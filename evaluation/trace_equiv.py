#!/usr/bin/env python3
"""Trace Equiv.: can the generated model execute the gold attack?

The gold counterexample is replayed in each generated model. It is taken in full from modelCheck on the gold rules
and the gold checker: the prefix and one round of the cycle, with every event. The trace that run_all_e2e.py writes
to comparison.md comes from lib/postProcess.maude, which prints only the prefix and drops events that change no
state; in Imou the attacker's bind is in the cycle, so that trace stops before the attack completes.
  1. Its events (subject, action, object) are renamed into the generated vocabulary by inverting the model's mapping
     (evaluation/mappings/). A gold name that several generated names map to may be any of them. Data arguments
     are left free, so the generated model computes them itself. An event whose action has no generated counterpart
     is skipped.
  2. The events are replayed in order and any of them may be skipped (flaw_repro.replay_events): the gold attack is
     present if some subsequence of the gold trace, in its order, is an execution of the generated model that
     violates the generated property. Skipping is needed because the gold trace also contains steps unrelated to the
     attack and, after the violation, the loop Maude prints to close the counterexample.
  3. The generated property is the generated checker: the same template, the slot propositions Agent_P wrote, and
     attackerActs. Whether those propositions are right is measured separately (propositions.py, flaw_repro.py).
A run whose model did not load scores 0. Trace Equiv. per protocol = runs with the gold attack / runs, in percent;
the All row averages the protocols.
Writes per_run.csv, per_protocol.csv, summary.json, table.md and details/<protocol>.md to OUT_DIR.
Usage: python evaluation/trace_equiv.py [--jobs N] [OUT_DIR]   (default evaluation/results/trace_equiv)
"""
import argparse, csv, hashlib, json, re, shutil, statistics, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import flaw_repro as F  # noqa: E402
from validate_property_templates import GOLD  # noqa: E402
from propositions import gen_parts  # noqa: E402

EVENT = re.compile(r"\$ (\S+) ('[^']*') ([^\s,|})]+)")


def gold_trace(binary, lib, protocol, work):
    """Every event (subject, action, object) of the gold counterexample: the prefix, then one round of the cycle."""
    golden = F.GOLDEN_NAME.get(protocol, protocol)
    d = work / f'gold-{golden}'
    d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(GOLD / golden / 'rules.maude', d / 'rules.maude')
    checker = re.sub(r'^load \.\./lib/postProcess \.\s*$', 'red modelCheck(init, spec) .\nquit .',
                     (GOLD / golden / 'checker.maude').read_text(), flags=re.M)
    (d / 'checker.maude').write_text(checker)
    out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', 'checker.maude'],
                         stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=d, timeout=600,
                         env={'MAUDE_LIB': str(lib), 'PATH': '/usr/bin:/bin'}).stdout
    result = out.split('result ModelCheckResult:', 1)[-1].strip()
    if not result.startswith('counterexample('):
        raise SystemExit(f'{protocol}: the gold checker gives no counterexample')
    return EVENT.findall(result)


def inverse(mapping, category):
    inv = {}
    for gen, gold in mapping[category].items():
        if gold is not None:
            inv.setdefault(gold, []).append(gen)
    return inv


def rename(events, mapping):
    pinv, ainv = inverse(mapping, 'principals'), inverse(mapping, 'actions')
    return [(pinv.get(s, [s]), ainv.get(a, []), pinv.get(o, [o])) for s, a, o in events]


def generated_module(run_dir, protocol, subtype, attacker):
    checker = (run_dir / protocol / 'checker.maude').read_text()
    patterns, sorts = gen_parts(checker)
    decls = '\n'.join(f'vars {v} : {s} .' for v, s in sorts.items())
    forbid = bool(re.search(r'eq basic = .*~ sp', checker))
    return F.property_module(subtype, attacker, patterns, decls, forbid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/trace_equiv'))
    ap.add_argument('--jobs', type=int, default=8)
    a = ap.parse_args()
    out = Path(a.out).resolve()
    runs = [l.split(None, 1) for l in (HERE / 'runs.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
    binary, lib = F.maudeBinary()
    work = Path(tempfile.mkdtemp(prefix='traceequiv-'))
    (work / 'lib').symlink_to(ROOT / 'lib')
    gold_work = Path(tempfile.mkdtemp(prefix='goldtrace-'))
    (gold_work / 'lib').symlink_to(GOLD / 'lib')
    traces = {}
    items = []
    for name, d in runs:
        d = ROOT / d.strip()
        for r in json.loads((d / 'summary.json').read_text()):
            p = r['protocol']
            golden = F.GOLDEN_NAME.get(p, p)
            if p not in traces:
                traces[p] = gold_trace(binary, lib, p, gold_work)
            item = dict(protocol=p, run=name, status=r['status'], gold=traces[p], events=[])
            if r['status'] == 'validated':
                rules = d / p / 'rules.maude'
                sha = hashlib.sha256(rules.read_bytes()).hexdigest()
                mapping = json.loads((HERE / 'mappings' / p / f'{sha[:12]}.json').read_text())['mapping']
                subtype, _, attacker = F.MAPPING[golden]
                item.update(events=rename(item['gold'], mapping), rules=rules,
                            module=generated_module(d, p, subtype, attacker), key=f'{p}-{sha[:12]}')
            items.append(item)
    jobs = {i['key']: i for i in items if i['events']}
    run = lambda i: F.replay_events(binary, lib, i['rules'], i['module'], i['events'], work / i['key'])
    with ThreadPoolExecutor(a.jobs) as ex:
        results = dict(zip(jobs, ex.map(run, jobs.values())))
    for i in items:
        res, err = results.get(i.get('key'), (False, ''))
        i['present'], i['error'] = bool(res), err if res is None else ''
        i['label'] = ('model did not load' if i['status'] != 'validated' else 'error' if res is None else
                      'gold attack present' if res else 'gold attack not present')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'details').mkdir(exist_ok=True)
    rows = [dict(protocol=i['protocol'], run=i['run'], label=i['label'], gold_events=len(i['gold']),
                 unmatched_actions=sum(not e[1] for e in i['events'])) for i in items]
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    protocols = sorted({i['protocol'] for i in items}, key=str.lower)
    per = []
    for p in protocols:
        sel = [i for i in items if i['protocol'] == p]
        k = sum(i['present'] for i in sel)
        per.append(dict(protocol=p, runs=len(sel), present=k, trace_equiv=round(100 * k / len(sel), 1)))
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    overall = round(statistics.mean(p['trace_equiv'] for p in per), 1)
    table = ['| Protocol | Gold attack present | Trace Equiv. (%) |', '|---|---|---|']
    table += [f"| {F.DISPLAY.get(p['protocol'], p['protocol'])} | {p['present']}/{p['runs']} | {p['trace_equiv']} |"
              for p in per]
    table.append(f'| **All ({len(per)}), mean of protocols** | {sum(p["present"] for p in per)}/'
                 f'{sum(p["runs"] for p in per)} | {overall} |')
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    labels = {}
    for i in items:
        labels[i['label']] = labels.get(i['label'], 0) + 1
    (out / 'summary.json').write_text(json.dumps(dict(runs=dict(runs), trace_equiv=overall, labels=labels), indent=2) + '\n')
    for p in protocols:
        sel = [i for i in items if i['protocol'] == p]
        body = [f'# {p}: gold counterexample replayed in the generated models', '',
                'Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):', '']
        body += [f'{k + 1}. `{s} {act} {o}`' for k, (s, act, o) in enumerate(sel[0]['gold'])] + ['']
        for i in sel:
            body += [f"## {i['run']}: {i['label']}" + (f" ({i['error']})" if i['error'] else ''), '']
            unmatched = [f'{k + 1}' for k, e in enumerate(i['events']) if not e[1]]
            if unmatched:
                body += [f"gold events without a generated action (skipped): {', '.join(unmatched)}", '']
        (out / 'details' / f'{p}.md').write_text('\n'.join(body))
    print('\n'.join(table))
    print(f'\nlabels: {labels}')
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(gold_work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Performance: time, tokens, state space and counterexample length per protocol.

  Time (s)     <protocol>/run.json elapsed_seconds: the whole pipeline for one protocol (every LLM call, the Maude
               validation and the model check), wall clock; mean over the runs. Maude takes about 0.5 s of it.
  Tokens (k)   <protocol>/run.json tokens_this_run: total tokens (input and output) of every LLM call in the run,
               retries included; mean over the runs, in thousands
  States       distinct system states S reachable within the checker bound: a copy of rules.maude in which every
               rule fires only from a state with counter < 5 and time < 3 (the bound of every checker, boundReached),
               then 'search init =>* V:Vertex' lists every reachable vertex E @ S. A vertex also records the event E
               that led to it, so the same system state reached by different events is one state here (the vertices
               are kept in the CSV). Mean over the runs whose model loaded; the gold model is counted the same way.
  Trace        <protocol>/run.json check.events: the number of events of the counterexample the pipeline reported
               (counterexample.txt); mean over the runs that returned a counterexample, "--" if none did. It is the
               first counterexample of Maude's depth-first search, not the shortest, so it depends on rule order.
A run whose model did not load still counts for time and tokens. The All row averages the protocols (states and trace
length only over the protocols that have them).
Writes per_run.csv, per_protocol.csv and table.md to OUT_DIR.
Usage: python evaluation/performance.py [--jobs N] [OUT_DIR]   (default evaluation/results/performance)
"""
import argparse, csv, json, re, statistics, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_property_templates import maudeBinary  # noqa: E402

DISPLAY = {'philips': 'Philips Hue'}
GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}
BOUND = """
op bnd : Soup -> Bool .
var BndN : Nat . var BndS : Soup . var BndA : Set .
ceq bnd(< system | ('counter' : BndN , BndA) > BndS) = true if BndN >= 5 .
ceq bnd(< system | ('time' : BndN , BndA) > BndS) = true if BndN >= 3 .
eq bnd(BndS) = false [owise] .
"""
RULE = re.compile(r'^rl (\[[^\]]+\]): E @ (.*?)\n=> (.*?) \.$', re.M | re.S)


def bounded(text):
    """rules.maude with every rule guarded by bnd(left-hand soup) = false."""
    head, trans = text.split('mod TRANSITION is', 1)
    rules = len(re.findall(r'^c?rl \[', trans, re.M))
    trans, n = RULE.subn(lambda m: f'crl {m.group(1)}: E @ {m.group(2)}\n=> {m.group(3)} '
                                   f'if bnd({m.group(2).strip()}) = false .', trans)
    if n != rules:
        raise ValueError(f'guarded {n} of {rules} rules')
    return head + 'mod TRANSITION is' + trans.replace('including SYSTEM .', 'including SYSTEM .' + BOUND, 1)


def states(binary, lib, rules, model_lib, timeout=600):
    """(distinct system states, vertices) reachable within the checker bound, or None (with the reason)."""
    d = Path(tempfile.mkdtemp(prefix='states-')) / 'm'
    d.mkdir(parents=True)
    (d.parent / 'lib').symlink_to(Path(model_lib).resolve())
    try:
        (d / 'rules.maude').write_text(bounded(Path(rules).read_text()))
    except ValueError as e:
        return None, str(e)
    (d / 'run.maude').write_text('load rules .\nsearch in TRANSITION : init =>* V:Vertex .\nquit .\n')
    try:
        out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', 'run.maude'],
                             capture_output=True, text=True, cwd=d, timeout=timeout,
                             env={'MAUDE_LIB': str(lib), 'PATH': '/usr/bin:/bin'})
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    vertices = [' '.join(v.split()) for v in re.findall(r'V:Vertex --> (.*?)(?=\n\nSolution|\n\nNo more|\Z)', out.stdout, re.S)]
    if 'No more solutions' not in out.stdout or not vertices:
        return None, out.stdout[-300:]
    return (len({v.split(' @ ', 1)[1] for v in vertices}), len(vertices)), ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/performance'))
    ap.add_argument('--jobs', type=int, default=8)
    a = ap.parse_args()
    out = Path(a.out)
    runs = [l.split(None, 1) for l in (HERE / 'runs.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
    binary, lib = maudeBinary()
    rows = []
    for name, d in runs:
        d = ROOT / d.strip()
        for r in json.loads((d / 'summary.json').read_text()):
            m = json.loads((d / r['protocol'] / 'run.json').read_text())
            check = m.get('check') or {}
            rows.append(dict(protocol=r['protocol'], run=name, status=m['status'], time_s=m['elapsed_seconds'],
                             tokens=m['tokens_this_run'], rules=str(d / r['protocol'] / 'rules.maude'),
                             verdict=check.get('verdict', ''),
                             trace=check['events'] if check.get('verdict') == 'counterexample' else ''))
    names = sorted({r['protocol'] for r in rows}, key=str.lower)
    jobs = [(r['rules'], ROOT / 'lib') for r in rows if r['status'] == 'validated']
    jobs += [(GOLD / GOLDEN_NAME.get(p, p) / 'rules.maude', GOLD / 'lib') for p in names]
    with ThreadPoolExecutor(a.jobs) as ex:
        counted = dict(zip([str(j[0]) for j in jobs], ex.map(lambda j: states(binary, lib, *j), jobs)))
    for r in rows:
        n, err = counted.get(r['rules'], ('', 'model did not load'))
        r.update(states=n[0] if n else '', vertices=n[1] if n else '', states_note=err)
        r.pop('rules')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    per = []
    for p in names:
        sel = [r for r in rows if r['protocol'] == p]
        traces = [r['trace'] for r in sel if r['trace'] != '']
        sts = [r['states'] for r in sel if r['states'] != '']
        gold, _ = counted[str(GOLD / GOLDEN_NAME.get(p, p) / 'rules.maude')]
        vts = [r['vertices'] for r in sel if r['vertices'] != '']
        per.append(dict(protocol=p, runs=len(sel), time_s=round(statistics.mean(r['time_s'] for r in sel), 1),
                        tokens_k=round(statistics.mean(r['tokens'] for r in sel) / 1000, 1),
                        states=round(statistics.mean(sts), 1) if sts else '', gold_states=gold[0] if gold else '',
                        vertices=round(statistics.mean(vts), 1) if vts else '', gold_vertices=gold[1] if gold else '',
                        counterexamples=len(traces), trace=round(statistics.mean(traces), 1) if traces else ''))
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    mean = lambda k: round(statistics.mean(p[k] for p in per if p[k] != ''), 1)
    table = ['| Protocol | Time (s) | Tokens (k) | States | Gold states | Trace (events) |', '|---|---|---|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['time_s']} | {p['tokens_k']} | {p['states'] or '--'} | "
              f"{p['gold_states'] or '--'} | {p['trace'] or '--'} |" for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | {mean('time_s')} | {mean('tokens_k')} | {mean('states')} | "
                 f"{mean('gold_states')} | {mean('trace')} |")
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    print('\n'.join(table))
    missing = [f"{r['protocol']} {r['run']}: {r['states_note']}" for r in rows
               if r['status'] == 'validated' and r['states'] == '']
    if missing:
        print('\nstates not counted: ' + '; '.join(missing))
    return 0


if __name__ == '__main__':
    sys.exit(main())

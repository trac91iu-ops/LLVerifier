#!/usr/bin/env python3
"""Export the material for the manual Trace Equiv. review: can the generated model execute the gold attack?

For each protocol:
  gold      the gold attack: the gold counterexample (modelCheck on the gold rules and checker) cut at the step
            where the gold property is violated (flaw_repro.reported_violation), with the attribute changes of every
            step; the gold property; the event rules of the gold model; the input diagram.
  models    one entry per distinct generated rules.maude (several runs may produce the same file), with its runs,
            the event rules, the name mapping (evaluation/mappings/), the generated property and, when the run
            reported one, its counterexample cut the same way. For every gold attack step, the generated event
            rules whose action maps to the gold action are listed as candidates.
  runs      every run with its load status; a run whose model did not load scores 0 and is not reviewed.
The script results of trace_equiv.py and flaw_repro.py are attached as hints.
Writes OUT (default evaluation/results/trace_equiv_review/data.json). The review page reads this file; the
judgements it stores are scored by trace_equiv_manual.py.
Usage: python evaluation/trace_equiv_review.py [--jobs N] [--runs FILE] [--no-mapping] [--skip PROTOCOL]...
                                                [--previous DATA VERDICTS] [OUT]
       --runs names the run list (default evaluation/runs.txt); --no-mapping leaves out the name mappings and the
       candidate rules derived from them (the reviewer reads the generated names); --skip leaves out a protocol (repeatable).
       e.g. the ablation without guardrail repair: --runs evaluation/runs-ablation-norepair.txt --no-mapping
       --skip CloudEdgeRTE evaluation/results/trace_equiv_review_norepair/data.json
       --previous DATA VERDICTS attaches an earlier verdict (export of an earlier review page) to every model whose
       rules, property and counterexample are identical to a model of the earlier DATA; the page shows it as a hint.
"""
import argparse, csv, hashlib, json, re, shutil, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import flaw_repro as F  # noqa: E402
from rules import parse_soup  # noqa: E402
from validate_property_templates import MAPPING, goldenParts  # noqa: E402
from property_templates import safetyFormula  # noqa: E402

FIDELITY = ROOT / 'sequence_diagram/input'  # same diagrams as eval-v1-20261102/fidelity-inputs, plus A2A


def event_text(state):
    return state.split(' @ ', 1)[0].strip()


def show(value):
    return '{' + ', '.join(value) + '}' if isinstance(value, tuple) else value


def changes(before, after):
    """Attribute changes from one state to the next, as 'path: old -> new' lines."""
    a, b = parse_soup(before.split(' @ ', 1)[1])[0], parse_soup(after.split(' @ ', 1)[1])[0]
    out = []
    for key in sorted(set(a) | set(b), key=str):
        if a.get(key) != b.get(key):
            old = show(a[key]) if key in a else '(none)'
            new = show(b[key]) if key in b else '(none)'
            out.append(f"{' . '.join(key)}: {old} -> {new}")
    return out


def steps(states, events):
    """The cut counterexample as steps: the event text and the attribute changes it made."""
    n = len(events)
    return [dict(event=event_text(states[k + 1]), changes=changes(states[k], states[k + 1])) for k in range(n)]


def transition_rules(text):
    """Event rules of the TRANSITION module: label, action, event equation and the rule text."""
    body = text.split('mod TRANSITION', 1)[1]
    evs = {m.group(1): (m.group(3), m.group(0).strip())
           for m in re.finditer(r"^eq (ev\d+)\((.*?)\) = (?:\$ \S+ ('[^']*')).*$", body, re.M)}
    out = []
    for m in re.finditer(r'^(c?rl \[(\w+)\]:.*?)(?=^c?rl \[|^endm|\Z)', body, re.M | re.S):
        rule = m.group(1).strip()
        ev = re.search(r'ep: (ev\d+)\(', rule)
        action, eq = evs.get(ev.group(1), (None, '')) if ev else (None, '')
        out.append(dict(label=m.group(2), action=action, equation=eq, text=rule))
    return out


def property_text(checker):
    keep = [l for l in checker.splitlines() if l.startswith(('*** ap', 'eq E @ S', 'ceq E @ S', 'eq safety'))
            and 'boundReached' not in l and '|= sp' not in l]
    return '\n'.join(keep)


def counterexample(binary, lib, rules, checker, mod, d):
    states = F.full_states(binary, lib, rules, checker, d)
    if states is None:
        return None
    events = F.reported_violation(binary, lib, rules, mod, states, d)
    return None if events is None else steps(states, events)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/trace_equiv_review/data.json'))
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--runs', default=str(HERE / 'runs.txt'))
    ap.add_argument('--no-mapping', action='store_true')
    ap.add_argument('--skip', action='append', default=[], metavar='PROTOCOL')
    ap.add_argument('--previous', nargs=2, metavar=('DATA', 'VERDICTS'))
    a = ap.parse_args()
    runs = [l.split(None, 1) for l in Path(a.runs).read_text().splitlines() if l.strip() and not l.startswith('#')]
    binary, lib = F.maudeBinary()
    gold_work = Path(tempfile.mkdtemp(prefix='review-gold-'))
    (gold_work / 'lib').symlink_to(F.GOLD / 'lib')
    gen_work = Path(tempfile.mkdtemp(prefix='review-gen-'))
    (gen_work / 'lib').symlink_to(ROOT / 'lib')
    hints = {}
    for name, path in [('script_trace', 'trace_equiv'), ('script_flaw', 'flaw_repro')]:
        for r in csv.DictReader(open(HERE / 'results' / path / 'per_run.csv')):
            hints.setdefault((r['protocol'], r['run']), {})[name] = r['label']

    protocols, jobs = {}, []
    for run, d in runs:
        d = ROOT / d.strip()
        for r in json.loads((d / 'summary.json').read_text()):
            p = r['protocol']
            if p in a.skip:
                continue
            golden = F.GOLDEN_NAME.get(p, p)
            subtype, slots, attacker = MAPPING[golden]
            if p not in protocols:
                patterns, _, _ = goldenParts(golden, slots)
                gold_rules = F.GOLD / golden / 'rules.maude'
                protocols[p] = dict(protocol=p, display=F.DISPLAY.get(p, p), subtype=subtype, attacker=attacker,
                                    diagram=(FIDELITY / p / 'diagram.md').read_text(),
                                    gold=dict(property=safetyFormula(subtype, patterns),
                                              slots=patterns, rules=transition_rules(gold_rules.read_text())),
                                    models={}, runs=[])
                jobs.append(('gold', p, gold_rules, F.GOLD / golden / 'checker.maude', F.module(p),
                             gold_work / golden))
            entry = dict(run=run, status=r['status'], verdict=r['verdict'], **hints.get((p, run), {}))
            protocols[p]['runs'].append(entry)
            if r['status'] != 'validated':
                continue
            rules = d / p / 'rules.maude'
            sha = hashlib.sha256(rules.read_bytes()).hexdigest()[:12]
            entry['model'] = sha
            models = protocols[p]['models']
            if sha not in models:
                mapping = None if a.no_mapping else json.loads((HERE / 'mappings' / p / f'{sha}.json').read_text())['mapping']
                checker = (d / p / 'checker.maude').read_text()
                models[sha] = dict(id=sha, runs=[], mapping=mapping, rules=transition_rules(rules.read_text()),
                                   property=property_text(checker), property_run=run, verdict=r['verdict'])
                if r['verdict'] == 'counterexample':
                    jobs.append(('gen', (p, sha), rules, d / p / 'checker.maude',
                                 F.generated_module(d, p, subtype, attacker), gen_work / f'{run}-{p}'))
            models[sha]['runs'].append(run)

    def work(job):
        kind, key, rules, checker, mod, d = job
        return kind, key, counterexample(binary, lib, rules, checker, mod, d)

    with ThreadPoolExecutor(a.jobs) as ex:
        for kind, key, cex in ex.map(work, jobs):
            if kind == 'gold':
                if cex is None:
                    raise SystemExit(f'{key}: the gold attack is not found')
                protocols[key]['gold']['attack'] = cex
            else:
                protocols[key[0]]['models'][key[1]]['counterexample'] = cex

    for p in protocols.values():
        for m in p['models'].values():
            if m['mapping'] is None:
                m['candidates'] = None
                continue
            inv = {}
            for gen, gold in m['mapping']['actions'].items():
                if gold is not None:
                    inv.setdefault(gold, []).append(gen)
            m['candidates'] = []
            for step in p['gold']['attack']:
                act = re.match(r"\$ \S+ ('[^']*')", step['event'])
                gens = inv.get(act.group(1), []) if act else []
                m['candidates'].append(dict(actions=gens,
                                            rules=[r['label'] for r in m['rules'] if r['action'] in gens]))
        p['models'] = list(p['models'].values())
    if a.previous:
        from trace_equiv_manual import load_verdicts
        verdicts = load_verdicts(a.previous[1])
        earlier = {(p['protocol'], m['id']): m for p in json.loads(Path(a.previous[0]).read_text())['protocols']
                   for m in p['models']}
        for p in protocols.values():
            for m in p['models']:
                old, v = earlier.get((p['protocol'], m['id'])), verdicts.get((p['protocol'], m['id']))
                if old and v and (old['property'], old.get('counterexample')) == (m['property'], m.get('counterexample')):
                    m['previous'] = dict(verdict=v['verdict'], note=v.get('note', ''))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = dict(runs=dict(runs), protocols=sorted(protocols.values(), key=lambda p: p['protocol'].lower()))
    out.write_text(json.dumps(data, indent=1) + '\n')
    models = sum(len(p['models']) for p in data['protocols'])
    previous = sum('previous' in m for p in data['protocols'] for m in p['models'])
    print(f'{out}: {len(data["protocols"])} protocols, {models} distinct generated models'
          + (f', {previous} with an earlier verdict' if a.previous else ''))
    shutil.rmtree(gold_work, ignore_errors=True)
    shutil.rmtree(gen_work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

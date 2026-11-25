#!/usr/bin/env python3
"""Flaw Repro.: does the counterexample of a generated model reproduce a violation of the gold property?

A returned counterexample is not enough: a wrong slot proposition can make the property trivially violated
(delegationFlaw2: legitimate use counted as an attack). So each generated counterexample is replayed in the gold model
and judged with the gold property:
  1. The counterexample is taken in full from modelCheck on the generated rules and checker: the prefix, then one
     round of the cycle, with every event. counterexample.txt is not used, since lib/postProcess.maude prints only the
     prefix and the attack can complete in the cycle (see trace_equiv.py). Its events are renamed into the gold
     vocabulary with the model's mapping (evaluation/mappings/): subject, action and object. Data arguments (keys,
     fresh values) are left free, so the gold model computes them itself.
  2. The step at which the generated checker sees the violation is found by evaluating the generated property on
     the states of the counterexample (the first k >= 1 with A at state k and B at state k+1). The events after it
     are dropped: the cycle often contains other behaviour, and in delegationFlaw2 it even contains the real attack,
     while the reported violation is legitimate use before the revocation.
  3. The remaining events are replayed in order on the gold rules, and any of them but the last may be skipped: the
     flaw is real if some subsequence of them, ending with the reported violating event, is an execution of the gold
     model whose last step violates the gold property. Skipping is needed because a counterexample also contains
     steps unrelated to the attack, and one of them can be impossible or change the state in the gold model (August:
     gold allows pressing the button only once, the diagram does not). Events whose action has no gold counterpart
     are skipped.
  4. The gold property is the template property filled with the gold slot propositions (the instance validated in
     scripts/validate_property_templates.py). Every template has the form <> (A /\\ O B): the replay reproduces the flaw
     if at some state k >= 1 A holds and at state k+1 B holds, with no state up to k+1 beyond the checker's bound (and
     no system event where the gold checker forbids them).
A run whose model did not load, or whose property held, does not reproduce the flaw. Per protocol,
  accuracy = runs whose counterexample is a real flaw / runs that returned a counterexample (none if no run did)
  recall   = runs whose counterexample is a real flaw / runs
The All row averages the protocols; accuracy only over the protocols that returned a counterexample.
Writes per_run.csv, per_protocol.csv, summary.json, table.md and details/<protocol>.md to OUT_DIR.
Usage: python evaluation/flaw_repro.py [--jobs N] [--runs FILE] [OUT_DIR]   (default evaluation/results/flaw_repro)
       --runs names the run list (default evaluation/runs.txt), e.g. evaluation/runs-ablation-norepair.txt
"""
import argparse, csv, hashlib, json, re, shutil, statistics, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'src'))
from validate_property_templates import MAPPING, goldenParts, maudeBinary  # noqa: E402
from property_templates import SUBTYPES, safetyFormula  # noqa: E402
sys.path.insert(0, str(HERE))
from propositions import gen_parts  # noqa: E402

GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}
DISPLAY = {'philips': 'Philips Hue'}


def literals(conj):
    """'~ a /\\ b' -> [('a', False), ('b', True)]"""
    out = []
    for part in conj.split('/\\'):
        part = part.strip().strip('()').strip()
        if part:
            out.append((part[1:].strip(), False) if part.startswith('~') else (part, True))
    return out


def split_safety(formula):
    """'<> (A /\\ O (B))' -> (literals of A, literals of B)"""
    body = formula.strip()[2:].strip()[1:-1]
    a, b = body.split(' O ', 1) if ' O ' in body else body.split('O (', 1)
    return literals(a.rstrip().rstrip('/\\')), literals(b.strip()[1:-1] if b.strip().startswith('(') else b)


def conj(lits):
    return ' and '.join(f'(V |= {n})' if pos else f'not (V |= {n})' for n, pos in lits)


def property_module(subtype, attacker, patterns, decls, forbid):
    """Maude module over the rules in ./rules.maude with the slot propositions and the tests the replay needs."""
    names = [n for n in list(SUBTYPES[subtype]['slots']) + list(SUBTYPES[subtype]['optional']) if n in patterns]
    formula = safetyFormula(subtype, patterns)
    if ' O ' not in formula and 'O (' not in formula:  # <> (R \/ T) (CTX): the attack is the first state where R or T holds
        a_def = 'true'
        b_def = ' or '.join(f'(V |= {n.strip()})' for n in formula.strip()[2:].strip()[1:-1].split('\\/'))
    else:
        a, b = split_safety(formula)
        a_def, b_def = conj(a), conj(b)
    props = [f'eq E @ S {patterns[n]} |= {n} = true .' for n in names]
    if SUBTYPES[subtype].get('event'):
        names.append('attackerActs')
        props.append(f'ceq E @ S |= attackerActs = true if subject(E) == {attacker} .')
    basic = 'not (V |= boundReached)' + (' and not (V |= sp)' if forbid else '')
    return '\n'.join([
        'load rules .', 'load model-checker .', 'mod REPLAY is', "pr TRANSITION * (sort State to State') .",
        'including SATISFACTION .', 'subsort Vertex < State .', 'vars N : Nat .', decls, 'var Vtx : Vertex .',
        'var V : Vertex .', 'var P : Prop .', 'var E : Event .', 'var S : Soup .',
        'vars .. ... .... ..... ...... ....... : Set .', 'ops boundReached sp : -> Prop .',
        f"ops {' '.join(names)} : -> Prop .", *props,
        'ceq E @ S |= sp = true if subject(E) == system .',
        "ceq E @ S < system | 'counter' : N , ... > |= boundReached = true if N >= 5 .",
        "ceq E @ S < system | 'time' : N , ... > |= boundReached = true if N >= 3 .",
        'eq Vtx |= P = false [owise] .',
        'op evOf : Vertex -> Event .', 'eq evOf(E @ S) = E .',
        'ops aHolds bHolds basicOk : Vertex -> Bool .',
        f'eq aHolds(V) = {a_def} .', f'eq bHolds(V) = {b_def} .', f'eq basicOk(V) = {basic} .',
        'endm']) + '\n'


def module(protocol):
    """property_module for the gold model of a protocol, with the gold slot propositions."""
    golden = GOLDEN_NAME.get(protocol, protocol)
    subtype, slots, attacker = MAPPING[golden]
    patterns, decls, forbid = goldenParts(golden, slots)
    return property_module(subtype, attacker, patterns, decls, forbid)


COMMAND = re.compile(r'^(?:reduce|search(?: \[[^\]]*\])?) in REPLAY : ', re.M)


def run_maude(binary, lib, d, mod, commands):
    (d / 'step.maude').write_text(mod + '\n'.join(commands) + '\nquit .\n')
    out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', 'step.maude'],
                         stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=d, timeout=600,
                         env={'MAUDE_LIB': str(lib), 'PATH': '/usr/bin:/bin'})
    own = [l for l in out.stderr.splitlines() if 'step.maude' in l or 'rules.maude' in l]
    chunks = COMMAND.split(out.stdout)[1:]
    if own or len(chunks) != len(commands):
        raise RuntimeError(('\n'.join(own) or out.stdout.strip())[-400:])
    return chunks


def solutions(chunk):
    """The V:Vertex terms of a search result, each on one line."""
    terms = re.findall(r'^V(?::Vertex)? --> (.*?)(?=\n\n|\nSolution|\nNo more|\nBye|\Z)', chunk, re.S | re.M)
    return [' '.join(t.split()) for t in terms]


def either(fn, names):
    """Maude condition fn(V) == name for one name or any of several."""
    names = [names] if isinstance(names, str) else list(names)
    return '(' + ' or '.join(f'{fn}(evOf(V:Vertex)) == {n}' for n in names) + ')'


def replay_events(binary, lib, rules, mod, events, d, last=False):
    """True if some subsequence of the events, taken in order, violates the property of mod in the model rules.

    Each event is (subjects, actions, objects); each part is a name or a list of alternative names, and an event with
    no action is skipped. The states reachable after the first k events (each one taken or skipped) are kept as a set.
    A violation is a step s -> s2 by one of the events with A at s (s not the initial state) and B at s2, all states
    within the bound. With last=True the violating step must be the last event, and the others may be skipped."""
    d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rules, d / 'rules.maude')
    frontier = {'init': False}  # state -> A holds there (False for the initial state)
    try:
        for n, (subj, act, obj) in enumerate(events):
            if not act:
                continue
            final = n == len(events) - 1
            states = list(frontier)
            match = (f"{either('subject', subj)} and {either('action', act)} and {either('object', obj)} "
                     f'and basicOk(V:Vertex)')
            cmds = [f'search {st} =>1 V:Vertex such that {match} .' for st in states]
            new = []
            for st, chunk in zip(states, run_maude(binary, lib, d, mod, cmds)):
                succ = solutions(chunk)
                new += [t for t in succ if t not in frontier and t not in new]
                if frontier[st] and succ and (final or not last):  # a violating step from st: a successor with B
                    res = run_maude(binary, lib, d, mod, [f'reduce bHolds({t}) .' for t in succ])
                    if any('result Bool: true' in r for r in res):
                        return True, ''
            if last and final:
                break
            if new:
                res = run_maude(binary, lib, d, mod, [f'reduce aHolds({t}) .' for t in new])
                frontier.update({t: 'result Bool: true' in r for t, r in zip(new, res)})
            if len(frontier) > 20000:
                return None, 'too many states'
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    except RuntimeError as e:
        return None, str(e)
    return False, ''


def replay(binary, lib, protocol, events, work):
    """replay_events in the gold model of the protocol, judged by the gold property."""
    key = hashlib.sha256(json.dumps([protocol, events]).encode()).hexdigest()[:16]
    return replay_events(binary, lib, GOLD / GOLDEN_NAME.get(protocol, protocol) / 'rules.maude', module(protocol),
                         events, work / key, last=True)


STATE = re.compile(r"\{(.*?), '[^\s{}]+\}", re.S)
LEADING_EVENT = re.compile(r"^\$ (\S+) ('[^']*') ([^\s,|})]+)")


def full_states(binary, lib, rules, checker, d):
    """The states of the counterexample of a model, each as a one-line term: the prefix, then one round of the cycle.
    Each state E @ S starts with the event E that led into it. None if the property holds."""
    d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(rules, d / 'rules.maude')
    text = re.sub(r'^load \.\./lib/postProcess \.\s*$', 'red modelCheck(init, spec) .\nquit .',
                  Path(checker).read_text(), flags=re.M)
    (d / 'checker.maude').write_text(text)
    out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', 'checker.maude'],
                         stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=d, timeout=900,
                         env={'MAUDE_LIB': str(lib), 'PATH': '/usr/bin:/bin'}).stdout
    result = out.split('result ModelCheckResult:', 1)[-1].strip()
    if not result.startswith('counterexample('):
        return None
    return [' '.join(m.group(1).split()) for m in STATE.finditer(result)]


def full_trace(binary, lib, rules, checker, d):
    """Every event (subject, action, object) of the counterexample of a model; None if the property holds."""
    states = full_states(binary, lib, rules, checker, d)
    return None if states is None else [m.groups() for m in map(LEADING_EVENT.match, states) if m]


def generated_module(run_dir, protocol, subtype, attacker):
    """property_module with the slot propositions of the generated checker."""
    checker = (run_dir / protocol / 'checker.maude').read_text()
    patterns, sorts = gen_parts(checker)
    decls = '\n'.join(f'vars {v} : {s} .' for v, s in sorts.items())
    forbid = bool(re.search(r'eq basic = .*~ sp', checker))
    return property_module(subtype, attacker, patterns, decls, forbid)


def reported_violation(binary, lib, rules, mod, states, d):
    """The events up to the step where the property of mod is first violated along the states, or None."""
    shutil.copyfile(rules, d / 'rules.maude')
    cmds = [f'reduce aHolds({t}) .' for t in states] + [f'reduce bHolds({t}) .' for t in states]
    res = ['result Bool: true' in r for r in run_maude(binary, lib, d, mod, cmds)]
    a, b = res[:len(states)], res[len(states):]
    first = 0 if 'eq aHolds(V) = true .' in mod else 1  # a CTX attack may already happen after the first event
    for k in range(first, len(states) - 1):
        if a[k] and b[k + 1]:
            return [m.groups() for m in map(LEADING_EVENT.match, states[1:k + 2]) if m]
    return None


def to_gold(events, mapping):
    """Rename (subject, action, object) events into gold names; action None if it has no gold counterpart."""
    pm = {k: v for k, v in mapping['principals'].items() if v is not None}
    am = mapping['actions']
    return [(pm.get(s, s), am.get(a), pm.get(o, o)) for s, a, o in events]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/flaw_repro'))
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--runs', default=str(HERE / 'runs.txt'), help='run list (default evaluation/runs.txt)')
    a = ap.parse_args()
    out = Path(a.out).resolve()
    runs = [l.split(None, 1) for l in Path(a.runs).read_text().splitlines() if l.strip() and not l.startswith('#')]
    binary, lib = maudeBinary()
    work = Path(tempfile.mkdtemp(prefix='flawrepro-'))
    (work / 'lib').symlink_to(GOLD / 'lib')
    gen_work = Path(tempfile.mkdtemp(prefix='gentrace-'))
    (gen_work / 'lib').symlink_to(ROOT / 'lib')
    items, traces = [], []
    for name, d in runs:
        d = ROOT / d.strip()
        for r in json.loads((d / 'summary.json').read_text()):
            p = r['protocol']
            item = dict(protocol=p, run=name, verdict=r['verdict'], events=[])
            if r['verdict'] == 'counterexample':
                sha = hashlib.sha256((d / p / 'rules.maude').read_bytes()).hexdigest()
                item['mapping'] = json.loads((HERE / 'mappings' / p / f'{sha[:12]}.json').read_text())['mapping']
                traces.append((item, d / p / 'rules.maude', d / p / 'checker.maude', gen_work / f'{name}-{p}'))
            items.append(item)
    def reported(t):
        item, rules, checker, d = t
        states = full_states(binary, lib, rules, checker, d)
        if states is None:
            raise SystemExit(f"{item['protocol']} {item['run']}: no counterexample when model checked again")
        golden = GOLDEN_NAME.get(item['protocol'], item['protocol'])
        subtype, _, attacker = MAPPING[golden]
        mod = generated_module(rules.parent.parent, item['protocol'], subtype, attacker)
        return reported_violation(binary, lib, rules, mod, states, d)

    with ThreadPoolExecutor(a.jobs) as ex:
        prefixes = list(ex.map(reported, traces))
    for (item, *_), events in zip(traces, prefixes):
        if events is None:
            raise SystemExit(f"{item['protocol']} {item['run']}: the violation is not found on the counterexample states")
        item['events'] = to_gold(events, item['mapping'])
    jobs = {json.dumps([i['protocol'], i['events']]): i for i in items if i['events']}
    with ThreadPoolExecutor(a.jobs) as ex:
        results = dict(zip(jobs, ex.map(lambda i: replay(binary, lib, i['protocol'], i['events'], work), jobs.values())))
    for i in items:
        res, err = results.get(json.dumps([i['protocol'], i['events']]), (False, ''))
        i['reproduced'], i['error'] = bool(res), err if res is None else ''
        i['label'] = ('error' if res is None else 'reproduced' if res else
                      'not reproduced' if i['verdict'] == 'counterexample' else f"no counterexample ({i['verdict']})")
    out.mkdir(parents=True, exist_ok=True)
    (out / 'details').mkdir(exist_ok=True)
    rows = [dict(protocol=i['protocol'], run=i['run'], verdict=i['verdict'], label=i['label'], events=len(i['events']),
                 unmapped=sum(e[1] is None for e in i['events'])) for i in items]
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    protocols = sorted({i['protocol'] for i in items}, key=str.lower)
    per = []
    for p in protocols:
        sel = [i for i in items if i['protocol'] == p]
        cex, real = sum(i['verdict'] == 'counterexample' for i in sel), sum(i['reproduced'] for i in sel)
        # accuracy: reported counterexamples that are real flaws; recall: runs that report the real flaw
        per.append(dict(protocol=p, runs=len(sel), counterexample=cex, reproduced=real,
                        acc=round(100 * real / cex, 1) if cex else None, rec=round(100 * real / len(sel), 1)))
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    accs = [p['acc'] for p in per if p['acc'] is not None]
    overall = dict(acc=round(statistics.mean(accs), 1), rec=round(statistics.mean(p['rec'] for p in per), 1),
                   protocols_with_counterexample=len(accs))
    show = lambda x: '--' if x is None else x
    table = ['| Protocol | Counterexample | Real flaw | Acc. | Rec. |', '|---|---|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['counterexample']}/{p['runs']} | "
              f"{p['reproduced']}/{p['runs']} | {show(p['acc'])} | {p['rec']} |" for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | {sum(p['counterexample'] for p in per)} | "
                 f"{sum(p['reproduced'] for p in per)} | {overall['acc']} | {overall['rec']} |")
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    labels = {}
    for i in items:
        labels[i['label']] = labels.get(i['label'], 0) + 1
    (out / 'summary.json').write_text(json.dumps(dict(runs=dict(runs), labels=labels, mean_of_protocols=overall,
                                                      reproduced=sum(p['reproduced'] for p in per)), indent=2) + '\n')
    for p in protocols:
        body = [f'# {p}: generated counterexamples replayed in the gold model', '']
        for i in items:
            if i['protocol'] != p:
                continue
            body += [f"## {i['run']}: {i['label']}", '']
            body += [f'{k + 1}. `{s} {act if act else "(no gold action, skipped)"} {o}`'
                     for k, (s, act, o) in enumerate(i['events'])]
            body += ([f"error: {i['error']}"] if i['error'] else []) + ['']
        (out / 'details' / f'{p}.md').write_text('\n'.join(body))
    print('\n'.join(table))
    print(f'\nlabels: {labels}')
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(gen_work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

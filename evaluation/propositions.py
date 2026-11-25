#!/usr/bin/env python3
"""Propositions accuracy and recall: compare the slot propositions that Agent_P generated with those of the gold model.

The property template (its temporal structure) is fixed by the program, so the generated part of a property is the
state proposition that fills each slot. The gold proposition of each slot is the one the template validation uses
(scripts/validate_property_templates.py, MAPPING). attackerActs is written by the program and is not compared.

Each generated proposition is renamed into the gold vocabulary with the model's mapping (names and value encodings,
evaluation/mappings/), then both propositions are evaluated on the reachable states of the gold model with Maude
search, up to DEPTH events and leaving out the states beyond the checker's bound (boundReached: counter >= 5 or
time >= 3), which the model checker never considers either. At depth 12 most gold state spaces are already complete;
Broadlink, Philips, Kevo and Netvue are unbounded and are cut there. For one slot
  precise   the generated proposition never holds where the gold proposition is false, and it holds somewhere
            if the gold proposition does (a proposition that never holds is not a precise copy of one that does)
  recalled  the gold proposition never holds where the generated proposition is false
  accuracy = precise generated slots / generated slots;  recall = recalled gold slots / gold slots
Each slot is also labelled literal (same text after renaming), same meaning (precise and recalled, written
differently) or different. Per protocol the five runs are averaged; the All row averages the protocols.
Writes per_run.csv, per_protocol.csv, summary.json, table.md and details/<protocol>.md to OUT_DIR.
Usage: python evaluation/propositions.py [--jobs N] [OUT_DIR]   (default evaluation/results/propositions)
"""
import argparse, csv, hashlib, json, re, shutil, statistics, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'scripts'))
import rules as R  # noqa: E402
from validate_property_templates import MAPPING, TEMPLATE_VARS, goldenParts, maudeBinary  # noqa: E402

GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}
DISPLAY = {'philips': 'Philips Hue'}
PROGRAM_SLOTS = {'attackerActs'}
DEPTH = 12
CATEGORIES = ('attributes', 'principals', 'constants')
VAR = re.compile(r'[A-Z]\w*')


def gen_parts(checker):
    """Slot -> state pattern, and variable declarations, of a generated checker."""
    live = checker.split('mod CHECK')[0]
    patterns = {m.group(2): m.group(1).strip()
                for m in re.finditer(r'^eq E @ S (.*?)\s*\|= (\w+) = true \.', live, re.M)
                if m.group(2) not in PROGRAM_SLOTS | {'sp', 'boundReached'}}
    sorts = {}
    for line in re.findall(r'^vars? .+ : \w+ \.$', live, re.M):
        names, sort = line.split(':')
        for n in names.split()[1:]:
            if n not in TEMPLATE_VARS:
                sorts[n] = sort.strip().rstrip(' .')
    return patterns, sorts


def value_pattern(gen, gold):
    """Regex for a generated value and a function giving its gold value. A value written with variables (Kevo:
    ('owner' : UserX , Owners) for UserX) is a template: each variable matches one token and the gold value is filled
    in from them. Otherwise, or when the gold value uses a variable that the generated one does not bind, it is literal."""
    toks, gold_toks = gen.split(), gold.split()
    holes = {t for t in toks if VAR.fullmatch(t)}
    if not holes or any(VAR.fullmatch(t) and t not in holes for t in gold_toks):
        return re.escape(gen), lambda m: gold
    seen, parts = set(), []
    for t in toks:
        parts.append(re.escape(t) if t not in holes else f'(?P={t})' if t in seen else rf'(?P<{t}>[^\s,()]+)')
        seen.add(t)
    return ' '.join(parts), lambda m: ' '.join(m.group(t) if t in holes else t for t in gold_toks)


def translate(pattern, sorts, mapping):
    """Rename a generated pattern into the gold vocabulary; generated variables get a G suffix."""
    names = {k: v for c in CATEGORIES for k, v in mapping[c].items() if v is not None}
    names.update({v: v + 'G' for v in sorts})
    text = R.rename_tok(pattern, names)
    for v in mapping.get('values', []):
        value, gold = value_pattern(R.norm(v['generated']), R.norm(v['gold']))
        text = re.sub(rf"({re.escape(R.norm(v['attribute']))} : ){value}(?=\s|,|\))",
                      lambda m, gold=gold: m.group(1) + gold(m), text)
    decls = '\n'.join(f'vars {v}G : {s} .' for v, s in sorts.items() if re.search(rf'\b{v}G\b', text))
    return text, decls


def maude_check(binary, lib, protocol, gold_pat, gold_decls, gen_pat, gen_decls, work):
    """(gen satisfiable, gen without gold, gold without gen, gold satisfiable) on the gold model; None on error."""
    key = hashlib.sha256('\n'.join([protocol, gold_pat, gen_pat]).encode()).hexdigest()[:16]
    d = work / key
    d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(GOLD / GOLDEN_NAME.get(protocol, protocol) / 'rules.maude', d / 'rules.maude')
    inside = 'not (V:Vertex |= bound)'
    searches = [f'(V:Vertex |= genP) and {inside}', f'(V:Vertex |= genP) and not (V:Vertex |= goldP) and {inside}',
                f'(V:Vertex |= goldP) and not (V:Vertex |= genP) and {inside}', f'(V:Vertex |= goldP) and {inside}']
    (d / 'check.maude').write_text('\n'.join([
        'load rules .', 'load model-checker .', 'mod PROPCHECK is', "pr TRANSITION * (sort State to State') .", 'including SATISFACTION .',
        'subsort Vertex < State .', 'var Vtx : Vertex .', 'var P : Prop .', 'var E : Event .', 'var S : Soup .',
        'vars .. ... .... ..... ...... ....... : Set .', 'var BoundN : Nat .', gold_decls, gen_decls,
        'ops goldP genP bound : -> Prop .',
        "ceq E @ S < system | 'counter' : BoundN , ... > |= bound = true if BoundN >= 5 .",
        "ceq E @ S < system | 'time' : BoundN , ... > |= bound = true if BoundN >= 3 .",
        f'eq E @ S {gold_pat} |= goldP = true .', f'eq E @ S {gen_pat} |= genP = true .',
        'eq Vtx |= P = false [owise] .', 'endm',
        *[f'search [1, {DEPTH}] init =>* V:Vertex such that {s} .' for s in searches], 'quit .']) + '\n')
    try:
        out = subprocess.run([str(binary), '-no-banner', '-no-advise', '-no-wrap', '-no-ansi-color', 'check.maude'],
                             stdin=subprocess.DEVNULL, capture_output=True, text=True, cwd=d, timeout=600,
                             env={'MAUDE_LIB': str(lib), 'PATH': '/usr/bin:/bin'})
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    parts = re.split(r'search (?:\[[^\]]*\] )?in PROPCHECK', out.stdout)[1:]
    own = [l for l in out.stderr.splitlines() if 'check.maude' in l or 'rules.maude' in l]
    if len(parts) != 4 or own:
        return None, ('\n'.join(own) or out.stdout.strip())[-400:]
    found = ['Solution 1' in p for p in parts]
    return (found[0], found[1], found[2], found[3]), ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default=str(HERE / 'results/propositions'))
    ap.add_argument('--jobs', type=int, default=8)
    a = ap.parse_args()
    out = Path(a.out).resolve()
    runs = [l.split(None, 1) for l in (HERE / 'runs.txt').read_text().splitlines() if l.strip() and not l.startswith('#')]
    binary, lib = maudeBinary()
    work = Path(tempfile.mkdtemp(prefix='propcheck-'))
    (work / 'lib').symlink_to(GOLD / 'lib')
    items, unreviewed = [], set()
    for name, d in runs:
        d = ROOT / d.strip()
        summary = {r['protocol']: r for r in json.loads((d / 'summary.json').read_text())}
        for protocol in sorted(summary, key=str.lower):
            golden = GOLDEN_NAME.get(protocol, protocol)
            subtype, slots, _ = MAPPING[golden]
            gold_pats, gold_decls, _ = goldenParts(golden, slots)
            sha = hashlib.sha256((d / protocol / 'rules.maude').read_bytes()).hexdigest()
            mfile = HERE / 'mappings' / protocol / f'{sha[:12]}.json'
            m = json.loads(mfile.read_text())
            if not m['reviewed']:
                unreviewed.add(mfile.name)
            checker = d / protocol / 'checker.maude'
            gen_pats, sorts = gen_parts(checker.read_text()) if checker.exists() else ({}, {})
            for slot in slots:
                gen = gen_pats.get(slot)
                text, decls = translate(gen, sorts, m['mapping']) if gen else (None, '')
                items.append(dict(protocol=protocol, run=name, loaded=summary[protocol]['status'] == 'validated',
                                  subtype=subtype, slot=slot, gold=gold_pats[slot], gold_decls=gold_decls,
                                  generated=gen, translated=text, gen_decls=decls))
    jobs = {(i['protocol'], i['gold'], i['translated']): i for i in items if i['translated']}
    with ThreadPoolExecutor(a.jobs) as ex:
        results = dict(zip(jobs, ex.map(lambda i: maude_check(binary, lib, i['protocol'], i['gold'], i['gold_decls'],
                                                              i['translated'], i['gen_decls'], work), jobs.values())))
    for i in items:
        res, err = results.get((i['protocol'], i['gold'], i['translated']), (None, 'not generated'))
        i['error'] = err
        if res is None:
            i.update(precise=False, recalled=False, label='not generated' if not i['generated'] else 'error')
            continue
        gen_sat, gen_only, gold_only, gold_sat = res
        i.update(gen_satisfiable=gen_sat, gold_satisfiable=gold_sat, precise=(gen_sat or not gold_sat) and not gen_only,
                 recalled=not gold_only)
        literal = R.norm(i['translated'].replace('G ', ' ')) == R.norm(i['gold'])
        i['label'] = ('literal' if literal and i['precise'] and i['recalled'] else
                      'same meaning' if i['precise'] and i['recalled'] else
                      'generated narrower' if i['precise'] else 'generated wider' if i['recalled'] and gen_sat
                      else 'different')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'details').mkdir(exist_ok=True)
    rows = []
    for name, _ in runs:
        for protocol in sorted({i['protocol'] for i in items}, key=str.lower):
            sel = [i for i in items if i['run'] == name and i['protocol'] == protocol]
            gen_slots = [i for i in sel if i['generated']]
            rows.append(dict(protocol=protocol, run=name, loaded=sel[0]['loaded'], gold_slots=len(sel),
                             gen_slots=len(gen_slots), precise=sum(i['precise'] for i in gen_slots),
                             recalled=sum(i['recalled'] for i in sel),
                             acc=round(100 * sum(i['precise'] for i in gen_slots) / len(gen_slots), 1) if gen_slots else 0.0,
                             rec=round(100 * sum(i['recalled'] for i in sel) / len(sel), 1),
                             labels=';'.join(f"{i['slot']}={i['label']}" for i in sel)))
    with open(out / 'per_run.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)

    def agg(sel):
        per = [dict(protocol=p, runs=len(rs), slots=rs[0]['gold_slots'],
                    acc=round(statistics.mean(r['acc'] for r in rs), 1), rec=round(statistics.mean(r['rec'] for r in rs), 1))
               for p in sorted({r['protocol'] for r in sel}, key=str.lower) for rs in [[r for r in sel if r['protocol'] == p]]]
        return per, dict(acc=round(statistics.mean(p['acc'] for p in per), 1), rec=round(statistics.mean(p['rec'] for p in per), 1))

    per, overall = agg(rows)
    _, overall_loaded = agg([r for r in rows if r['loaded']])
    with open(out / 'per_protocol.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, list(per[0])); w.writeheader(); w.writerows(per)
    table = ['| Protocol | Slots | Acc. | Rec. |', '|---|---|---|---|']
    table += [f"| {DISPLAY.get(p['protocol'], p['protocol'])} | {p['slots']} | {p['acc']} | {p['rec']} |" for p in per]
    table.append(f"| **All ({len(per)}), mean of protocols** | | {overall['acc']} | {overall['rec']} |")
    (out / 'table.md').write_text('\n'.join(table) + '\n')
    labels = {}
    for i in items:
        labels[i['label']] = labels.get(i['label'], 0) + 1
    (out / 'summary.json').write_text(json.dumps(dict(runs=dict(runs), mean_of_protocols=overall,
                                                      mean_of_protocols_loaded_runs_only=overall_loaded,
                                                      slot_labels=labels, unreviewed_mappings=len(unreviewed)), indent=2) + '\n')
    for protocol in sorted({i['protocol'] for i in items}, key=str.lower):
        body = [f'# {protocol}: slot propositions, generated vs. gold', '',
                'Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the '
                'generated proposition never holds where gold is false, and holds somewhere if gold does. '
                'recalled: gold never holds where the generated one is false.', '']
        seen = {}
        for i in items:
            if i['protocol'] != protocol:
                continue
            k = (i['slot'], i['translated'])
            if k in seen:
                seen[k]['runs'].append(i['run'])
                continue
            seen[k] = dict(i, runs=[i['run']])
        for (slot, _), i in seen.items():
            body += [f"## {slot}: {i['label']} ({', '.join(i['runs'])})", '', f"- gold: `{i['gold']}`",
                     f"- generated: `{i['generated']}`", f"- renamed: `{i['translated']}`",
                     f"- precise {i['precise']}, recalled {i['recalled']}" + (f"; error: {i['error']}" if i['error'] else ''), '']
        (out / 'details' / f'{protocol}.md').write_text('\n'.join(body))
    print('\n'.join(table))
    print(f'\nslot labels: {labels}\nloaded runs only: {overall_loaded}')
    errors = [i for i in items if i['label'] == 'error']
    if errors:
        print(f'\n{len(errors)} slots could not be checked, e.g. {errors[0]["protocol"]} {errors[0]["slot"]}: {errors[0]["error"]}')
    if unreviewed:
        print(f'\nWARNING: {len(unreviewed)} mappings not yet reviewed by a human (set "reviewed": true after checking).')
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

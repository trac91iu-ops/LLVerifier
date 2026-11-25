#!/usr/bin/env python3
"""Ask an LLM to propose, for every distinct generated model, which gold name each generated name corresponds to.

The mapping covers the names used by the state rules and the initial state (actions, attributes, principals and quoted
constants), plus the attribute values that the two models encode differently (e.g. true/false against 'on'/'off'). It only aligns names; whether the rules agree is decided later by state_trans.py. One file is written per
distinct generated model, evaluation/mappings/<protocol>/<sha256[:12]>.json, with "reviewed": false. A human checks
and edits the "mapping" field and sets "reviewed": true. Existing files are never overwritten, so human edits survive.
Usage: python evaluation/propose_mappings.py [--jobs N] [--model NAME] [--runs FILE] [PROTOCOL ...]
       --runs names the run list (default evaluation/runs.txt), e.g. evaluation/runs-ablation-norepair.txt
"""
import argparse, datetime, hashlib, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml
from openai import OpenAI

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import rules as R  # noqa: E402

GOLD = ROOT / 'benchmark/golden_data/formalModels'
GOLDEN_NAME = {'philips': 'Philips'}
CATEGORIES = ('actions', 'attributes', 'principals', 'constants')
ERROR_RETRY = 2

SYSTEM = """You align the vocabulary of two formal models of the same IoT protocol, written in Maude.
The gold model was written by experts. The generated model was written from the same protocol description by another \
author, who chose different names. For every name of the generated model, give the name of the gold model that plays \
the same role in the protocol, judged by what the name does in the rules (who sends a message, which attribute it \
reads or writes, what the value means), not by spelling. Use null when the gold model has no counterpart.
Several generated names may map to the same gold name when the generated model splits one gold concept. Map within \
the same category only. Do not judge whether the rules are correct; only align the names.
Also list the attributes whose values are encoded differently in the two models, for example a generated attribute \
with values true and false whose gold counterpart has values 'on' and 'off'. For each such value give the gold \
attribute name, the generated value and the gold value. Leave this list empty when the encodings agree.
Answer with one JSON object and nothing else, of the form
{"actions": {"<generated>": "<gold>" | null, ...}, "attributes": {...}, "principals": {...}, "constants": {...},
 "values": [{"attribute": "<gold attribute>", "generated": "<generated value>", "gold": "<gold value>"}, ...]}
with exactly the generated names listed in the request as keys."""


def system_module(path):
    text = path.read_text()
    m = re.search(r'^mod SYSTEM is\b.*?^endm', text, re.S | re.M)  # A2A has a comment after `is`
    return m.group(0)


def request(gold_path, gen_path, gold_inv, gen_inv):
    lines = ['Gold model:', '```', system_module(gold_path), '```', '', 'Generated model:', '```',
             system_module(gen_path), '```', '']
    for c in CATEGORIES:
        lines += [f'Generated {c}: ' + ', '.join(gen_inv[c]) if gen_inv[c] else f'Generated {c}: (none)',
                  f'Gold {c}: ' + ', '.join(gold_inv[c]) if gold_inv[c] else f'Gold {c}: (none)']
    return '\n'.join(lines)


def check(answer, gold_inv, gen_inv):
    """Error message for the LLM, or None if the mapping is well formed."""
    if not isinstance(answer, dict):
        return 'The answer must be one JSON object.'
    errs = []
    for c in CATEGORIES:
        got = answer.get(c, {})
        if not isinstance(got, dict):
            errs.append(f'"{c}" must be an object.')
            continue
        missing, extra = set(gen_inv[c]) - set(got), set(got) - set(gen_inv[c])
        if missing:
            errs.append(f'"{c}" is missing the generated names {sorted(missing)}.')
        if extra:
            errs.append(f'"{c}" has keys that are not generated {c}: {sorted(extra)}.')
        bad = sorted(v for v in got.values() if v is not None and v not in gold_inv[c])
        if bad:
            errs.append(f'"{c}" maps to names that are not gold {c}: {bad}.')
    values = answer.get('values', [])
    if not isinstance(values, list) or not all(isinstance(v, dict) and set(v) == {'attribute', 'generated', 'gold'}
                                               for v in values):
        errs.append('"values" must be a list of objects with the keys attribute, generated and gold.')
    else:
        bad = sorted({v['attribute'] for v in values} - set(gold_inv['attributes']))
        if bad:
            errs.append(f'"values" names attributes that are not gold attributes: {bad}.')
    return ' '.join(errs) or None


def parse(text):
    m = re.search(r'\{.*\}', text or '', re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def propose(job, client, model):
    protocol, gen_path, sha, runs, out = job
    gold_path = GOLD / GOLDEN_NAME.get(protocol, protocol) / 'rules.maude'
    gold_inv, gen_inv = R.inventory(R.load_model(gold_path)), R.inventory(R.load_model(gen_path))
    msgs = [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': request(gold_path, gen_path, gold_inv, gen_inv)}]
    attempts, tokens = [], 0
    for _ in range(1 + ERROR_RETRY):
        r = client.chat.completions.create(model=model, messages=msgs, temperature=0.1, top_p=0.1, max_tokens=32768,
                                           presence_penalty=0, frequency_penalty=0, n=1)
        text = r.choices[0].message.content
        tokens += r.usage.total_tokens if r.usage else 0
        answer = parse(text)
        err = check(answer, gold_inv, gen_inv) if answer is not None else 'The answer must be one JSON object.'
        attempts.append(dict(response=text, error=err))
        if err is None:
            break
        msgs += [{'role': 'assistant', 'content': text or ''}, {'role': 'user', 'content': f'{err} Answer again.'}]
    record = dict(protocol=protocol, model_sha256=sha, runs=runs, generated=str(gen_path.relative_to(ROOT)),
                  gold=str(gold_path.relative_to(ROOT)), reviewed=False, review_note='',
                  mapping=dict({c: answer.get(c, {}) for c in CATEGORIES}, values=answer.get('values', []))
                  if err is None else None,
                  gold_names=gold_inv, generated_names=gen_inv,
                  proposed_by=dict(model=model, at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                                   prompt_sha256=hashlib.sha256(SYSTEM.encode()).hexdigest()[:12], tokens=tokens,
                                   attempts=attempts))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
    return protocol, out.name, err


def jobs(protocols, runs_file):
    runs = [l.split(None, 1) for l in Path(runs_file).read_text().splitlines() if l.strip() and not l.startswith('#')]
    seen = {}
    for name, d in runs:
        for p in sorted((ROOT / d.strip()).iterdir()):
            f = p / 'rules.maude'
            if not f.exists() or (protocols and p.name not in protocols):
                continue
            sha = hashlib.sha256(f.read_bytes()).hexdigest()
            key = (p.name, sha)
            if key in seen:
                seen[key][3].append(name)
            else:
                seen[key] = [p.name, f, sha, [name], HERE / 'mappings' / p.name / f'{sha[:12]}.json']
    return [tuple(v) for v in seen.values()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('protocols', nargs='*')
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--model', default='codex-main')
    ap.add_argument('--runs', default=str(HERE / 'runs.txt'))
    a = ap.parse_args()
    prov = yaml.safe_load((ROOT / 'configs/config.yaml').read_text())['PROVIDERS']['codex']
    client = OpenAI(base_url=prov['base_url'], api_key=prov['api_key'], timeout=600)
    todo = [j for j in jobs(set(a.protocols), a.runs) if not j[4].exists()]
    print(f'{len(todo)} mappings to propose')
    with ThreadPoolExecutor(a.jobs) as ex:
        for protocol, name, err in ex.map(lambda j: propose(j, client, a.model), todo):
            print(f'{protocol:16} {name}  ' + ('ok' if err is None else f'FAILED: {err}'))


if __name__ == '__main__':
    main()

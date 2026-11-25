"""Replay genInit only (threat model + current diagram Notes), reusing the state templates logged in
sequence_diagram/output/full-20261028, and compare each init with the full-run init.
Usage: python scripts/replay_init.py OUT_DIR [protocol ...]
"""
import json, re, sys, copy
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'src')); sys.path.insert(0, str(ROOT / 'scripts'))
from Config import CONFIG
from LLMInterface import LLMSession
from diagram import splitDiagram, annotate
from threat_models import threatModel
import validate_property_templates as V
FULL = ROOT / 'sequence_diagram/output/full-20261028'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
CONFIG.LOGFILE = str(OUT / 'llm.log'); CONFIG.DEBUG = False

def canon(s):
    s = re.sub(r'```\w*', '', s).strip()
    toks = re.findall(r"'[^']*'|[()<>|,:]|[^\s()<>|,:']+", s)
    pos = 0
    def term():
        nonlocal pos
        items = [item()]
        while pos < len(toks) and toks[pos] == ',':
            pos += 1; items.append(item())
        return items[0] if len(items) == 1 else '(' + ' , '.join(sorted(items)) + ')'
    def item():
        nonlocal pos
        a = atom()
        if pos < len(toks) and toks[pos] == ':':
            pos += 1; return f'{a} : {atom()}'
        return a
    def atom():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == '(':
            v = term(); pos += 1  # ')'
            return v
        return t
    states = {}
    while pos < len(toks):
        assert toks[pos] == '<'; name = toks[pos + 1]; pos += 3
        states[name] = term(); pos += 1  # '>'
    return states

def safe(s):
    try: return canon(s)
    except Exception: return {'_unparsed': s}

def template(p):
    log = (FULL / p / 'llm.log').read_text()
    parts = log.split('[template]\n')
    return parts[3].split('\n\n[description]')[0].strip()

def oldInit(p):
    st = json.load(open(FULL / p / 'stages.json'))
    i = max(k for k, x in enumerate(st) if x.get('stage') == 'genInit')
    attempts = []
    for x in st[i + 1:]:
        if 'stage' in x: break
        attempts.append(x)
    return attempts[-1]['output']

def run(p):
    golden = {'philips': 'Philips'}.get(p, p)
    subtype = V.MAPPING[golden][0]
    text = (ROOT / 'sequence_diagram/input' / p / 'diagram.md').read_text()
    blocks = splitDiagram(text); desc = annotate(text, blocks) if blocks else text
    CONFIG.CACHEFILE = str(OUT / f'{p}.cache.json')
    llm = LLMSession(context_id=p); llm.source_context = desc
    if llm.hasCache(): llm.loadCache()
    new = llm.genInit(template(p), desc, threatModel(subtype))
    old = oldInit(p)
    a, b = safe(old), safe(new)
    diff = {k: (a.get(k), b.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)}
    return dict(protocol=p, subtype=subtype, same=not diff, diff=diff, old=old, new=new)

ps = sorted(d.name for d in (ROOT / 'sequence_diagram/input').iterdir() if (d / 'diagram.md').exists() and d.name != 'A2A')
ps = sys.argv[2:] or ps
with ThreadPoolExecutor(8) as ex:
    rows = list(ex.map(run, ps))
(OUT / 'summary.json').write_text(json.dumps(rows, indent=2))
for r in rows:
    print(f"{r['protocol']:16} {'SAME' if r['same'] else 'DIFF'}")
    for k, (o, n) in r['diff'].items():
        print(f'    {k}\n      old: {o}\n      new: {n}')

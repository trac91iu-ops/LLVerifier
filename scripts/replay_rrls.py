"""Replay genRRLs (state template and events from full-threat-20261028 logs) and count event rules per block.
Usage: python scripts/replay_rrls.py OUT_DIR PROTOCOL N BLOCKS SUBTYPE   e.g. ... delegationFlaw2 4 B2,B3 CTRL-direct
"""
import json, re, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'src'))
from Config import CONFIG
from LLMInterface import LLMSession
from diagram import splitDiagram, annotate
from prompts_text import block_label_instruction
from threat_models import threatModel
import checkers
OUT = Path(sys.argv[1]); P = sys.argv[2]; N = int(sys.argv[3]); WATCH = sys.argv[4].split(',')
CONFIG.LOGFILE = str(OUT / f'{P}.log'); CONFIG.CACHEFILE = str(OUT / 'none.json'); CONFIG.DEBUG = False
log = (ROOT / f'sequence_diagram/output/full-threat-20261028/{P}/llm.log').read_text()
sec = log.split('[state template]\n')[3]
template = sec.split('\n\n[events]\n')[0].strip()
events = sec.split('\n\n[events]\n')[1].split('\n\n[description]')[0].strip()
new = (ROOT / f'sequence_diagram/input/{P}/diagram.md').read_text()
old = (ROOT / f'record/code_change/2026-10-28-threat-model.before/input/{P}.diagram.md').read_text()
subtype = sys.argv[5]
def desc(t): b = splitDiagram(t); return annotate(t, b), [x.id for x in b]
COND = {'new': desc(new)}


def one(arg):
    k, i = arg
    d, ids = COND[k]
    llm = LLMSession(context_id=f'{k}{i}'); llm.source_context = d
    llm.mountChecker('genRRLs', checkers.labeled(checkers.checkTransitions, ids))
    out = llm.genRRLs(template, events, d + '\n\n' + block_label_instruction)
    labels = re.findall(r'\[(B\d+)\]', out)
    return k, {b: labels.count(b) for b in WATCH}, out
with ThreadPoolExecutor(12) as ex:
    res = list(ex.map(one, [(k, i) for k in COND for i in range(N)]))
for k in COND:
    print(k, [r for kk, r, _ in res if kk == k])
json.dump([(k, r, o) for k, r, o in res], open(OUT / f'{P}.json', 'w'), indent=1)

"""Replay genPolicyVars only, with the logged [protocol]/[formal]/[variables] of a run, and count the
sort chosen for one variable. Variants swap only the [protocol] text, so the formal rules stay fixed.
Usage: python scripts/replay_policy_vars.py OUT_DIR RUN_DIR VAR N name=diagram.md [name=diagram.md ...]
Set VARS_STRATEGY=<stage> to run genPolicyVars with that stage's model instead (e.g. genPolicy for the main model),
or VARS_DIRECT_MODEL=<model> (e.g. openai/gpt-6.1-sol) to send it straight to OpenCodex with reasoning_effort medium.
"""
import json, os, re, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'src'))
from Config import CONFIG
from LLMInterface import LLMSession
from Config import LLMProvider, Strategy
from diagram import splitDiagram, annotate

OUT, RUN, VAR, N = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
VARIANTS = dict(a.split('=', 1) for a in sys.argv[5:])
OUT.mkdir(parents=True, exist_ok=True)
CONFIG.LOGFILE = str(OUT / 'llm.log'); CONFIG.DEBUG = False

# the second LLM call of a run is genPolicyVars; its last user message holds the real input
call = (RUN / 'llm.log').read_text().split('---system---')[2]
user = call.split('---user---')[-1].split('---assistant---')[0]
formal = user.split('[formal]\n')[1].split('\n\n[variables]')[0]
variables = json.loads(user.split('[variables]\n')[1].strip().split('\n')[0].replace("'", '"'))

def protocol(path):
    """The [protocol] text exactly as synthesizeRules builds it: the diagram with block labels."""
    text = Path(path).read_text()
    return annotate(text, splitDiagram(text))

def one(args):
    name, i = args
    llm = LLMSession(); CONFIG.LOGFILE = str(OUT / f'{name}-{i}.log')
    if os.environ.get('VARS_STRATEGY'):
        llm.strategies['genPolicyVars'] = llm.strategies[os.environ['VARS_STRATEGY']]
    if os.environ.get('VARS_DIRECT_MODEL'):
        model = os.environ['VARS_DIRECT_MODEL']
        llm.providers['opencodex'] = LLMProvider(base_url='http://127.0.0.1:10100/v1/', api_key='local', models=[model])
        llm.strategies['genPolicyVars'] = Strategy(provider=('opencodex', model))
        configure = llm.configureParamsWithStrategy
        def withEffort(req, strategy):          # do what configs/litellm.yaml does for the codex aliases
            configure(req, strategy)
            for k in ('temperature', 'top_p', 'max_tokens', 'max_completion_tokens', 'presence_penalty',
                      'frequency_penalty', 'n', 'stop'):
                req.pop(k, None)
            req['reasoning_effort'] = 'medium'
        llm.configureParamsWithStrategy = withEffort
    return name, llm.genPolicyVars(protocol(VARIANTS[name]), formal, variables).get(VAR)

jobs = [(n, i) for n in VARIANTS for i in range(N)]
with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(one, jobs))
summary = {n: dict(Counter(t for m, t in results if m == n)) for n in VARIANTS}
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
for n, c in summary.items():
    print(f'{n:24} {VAR}: {c}')

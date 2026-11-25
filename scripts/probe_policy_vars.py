"""Ask genPolicyVars, with its exact prompt, to explain each type choice before the JSON (diagnosis only).
Usage: python scripts/probe_policy_vars.py OUT_DIR RUN_DIR DIAGRAM N
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / 'src'))
from Config import CONFIG
from LLMInterface import LLMSession
from prompts import policyVarsPromptTemplate
from diagram import splitDiagram, annotate

OUT, RUN, DIAGRAM, N = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
CONFIG.LOGFILE = str(OUT / 'llm.log'); CONFIG.DEBUG = False

call = (RUN / 'llm.log').read_text().split('---system---')[2]
user = call.split('---user---')[-1].split('---assistant---')[0]
formal = user.split('[formal]\n')[1].split('\n\n[variables]')[0]
variables = eval(user.split('[variables]\n')[1].strip().split('\n')[0])
text = DIAGRAM.read_text()
msg = policyVarsPromptTemplate(annotate(text, splitDiagram(text)), formal, variables)
msg[-1]['content'] += ('\n\nBefore the JSON, for each variable say in one or two sentences why you chose its type, '
                       'and whether the value it matches can be empty (nils) when the rule fires.')

def one(i):
    llm = LLMSession()      # same model as the stage: the genPolicyVars strategy
    return llm.askWithErrorHandling(msg, lambda a: None, strategy=llm.strategies['genPolicyVars'])

with ThreadPoolExecutor(N) as ex:
    answers = list(ex.map(one, range(N)))
(OUT / 'answers.md').write_text('\n\n---\n\n'.join(answers) + '\n')
print('\n\n---\n\n'.join(answers))

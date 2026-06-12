#!/bin/python3
from LLMInterface import LLMSession
from prompts import *
from utils import *
import sys

def testBaseline(llm, ipt):
    msg = baselinePrompt(ipt)
    r = llm.callAPI(msg)
    print(r)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'python {sys.argv[0]} <protocol_text_path>')
        exit(1)
    else:
        protocolFn = sys.argv[1]
    llm = LLMSession()
    protocol = fread(protocolFn)
    testBaseline(llm,protocol)

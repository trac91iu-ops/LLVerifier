#!/bin/python3
import os
import sys
import time
from utils import *
from Config import *
from synthesize import *
from LLMInterface import LLMSession

def persistant(project_name, file_name, content):
    outdir = CONFIG.OUTDIR
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    d = os.path.join(outdir,project_name)
    if not os.path.exists(d):
        os.mkdir(d)
    
    d2 = os.path.join(outdir, CONFIG.LIBDIR)
    if not os.path.exists(d2):
        os.symlink(CONFIG.LIBDIR, d2)
    
    fp = os.path.join(d,file_name)
    fwrite(fp, content)
    return fp

def inputParse(llm,txt):
    return llm.splitPolicy(txt)

def renameCache(project_name):
    try:
        d = os.path.dirname(CONFIG.CACHEFILE)
        p2 = os.path.basename(CONFIG.CACHEFILE).split('.json')[0]
        fn = p2+'_'+project_name+'.json'
        fullpath = os.path.join(d,fn)
        print(fullpath)
        os.system(f'cp {CONFIG.CACHEFILE} {fullpath}')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    HELP = 'python %s <protocol_text_path> [check|model]'
    if len(sys.argv) < 2:
        print(HELP % sys.argv[0])
        exit(1)
    else:
        protocolFn = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]
        if mode != 'check' or mode != 'model':
            print(HELP % sys.argv[0])
            exit(1)
    else:
        mode = 'check'

    PROJECT_NAME = os.path.basename(protocolFn)+'-'+str(int(time.time()))
    CONFIG.LOGFILE = os.path.join(CONFIG.LOGDIR, PROJECT_NAME+'.txt')

    print('[*] Split input file with LLM...')
    llm = LLMSession()
    if llm.hasCache():
        cmd = input('[*] Found cache file of a previous terminated execution, recover from it [y/n]?').strip()
        if cmd.lower() == 'y' or cmd == '':
            llm.loadCache()
        else:
            llm.deleteCache()
    
    if mode == 'model' or mode == 'check':
        EQ_desc,RRL_desc,init_desc,property_desc = inputParse(llm,fread(protocolFn))
        rules, state_template, events = synthesizeRules(llm,EQ_desc,RRL_desc,init_desc)
        fp = persistant(PROJECT_NAME, CONFIG.RULES_NAME, rules) 
        print(f'[+] Write to {fp} successfully')

    if mode == 'check':
        checker = synthesizeChecker(llm,property_desc,state_template,events)
        fp = persistant(PROJECT_NAME, CONFIG.CHECKER_NAME, checker) 
        print(f'[+] Write to {fp} successfully')
    
    print('[*] Total tokens consumed:',llm.tokens)
    if not CONFIG.DEBUG:
        renameCache(PROJECT_NAME)
        llm.deleteCache()

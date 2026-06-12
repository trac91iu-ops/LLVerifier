#!/bin/python3
import yaml
import os
from utils import *
import json
from pydantic import BaseModel, PositiveInt
from enum import Enum,auto
from typing import Optional

#ENUM
class MODE(str, Enum):
    USEWEB = "useweb"
    USEAPI = "useapi"

_DIRNAME = parentDir(os.path.dirname(os.path.abspath(__file__)))

def maskConfig(d):
    mask = lambda v: v[:5]+'x'*len(v[5:])
    for k,v in d.items():
        if isinstance(v,dict):
            maskConfig(v)
            continue
        elif k == 'api_key':
            d[k] = mask(v)

def maskConfigSafe(d):
    return maskConfig(d.copy())

class Strategy(BaseModel):
    provider: tuple[str,str]
    temperature: Optional[float] = 0 #deterministic
    top_p: Optional[float] = 0.1

class LLMProvider(BaseModel):
    base_url : str
    api_key : str
    models : list[str]
    proxy : Optional[str] = None

    def __str__(self):
        mask = lambda v: v[:5]+'x'*len(v[5:])
        sl = []
        for k,v in self.__dict__.items():
            if k == 'api_key':
                v = mask(v)
            sl.append(f"{k}={v}") 
        return ' '.join(sl)

class YAMLCONFIG(BaseModel):
    TIMEOUT_RETRY: PositiveInt = 3
    TOTAL_RETRY: PositiveInt = 2
    ERROR_RETRY: PositiveInt = 2
    N_CHOICES: PositiveInt = 1
    TEMPERATURE: float = 0
    VERBOSE: int = 1
    LOGDIR: str = 'logs'
    LOGFILE: str = 'log.txt'
    CACHEFILE: str = '.cache.json'
    OUTDIR: str = 'output'
    LIBDIR: str = 'lib'
    PROVIDERS: dict[str, LLMProvider]
    STRATEGIES: dict[str, Strategy]
    LOG: bool = True
    DEBUG : bool = False
    VERSION: str
    MODE : MODE 
    RULES_NAME : str = 'rule.maude'
    CHECKER_NAME : str = 'checker.maude'

class CONFIGCLS(YAMLCONFIG):
    CONFIG_FILE : Optional[str] = None 
    @staticmethod
    def load(config_file='config.yaml'):
        if not os.path.isabs(config_file):
            path = os.path.join(_DIRNAME, 'configs/', config_file)
        with open(path,'r') as f:
            c = yaml.safe_load(f)
        config = CONFIGCLS(**c)
        addDirPrefix = lambda x: os.path.join(_DIRNAME,x)
        if not os.path.isabs(config.LOGDIR):
            config.LOGDIR = addDirPrefix(config.LOGDIR)
        if not os.path.isabs(config.LOGFILE):
            config.LOGFILE = os.path.join(config.LOGDIR, config.LOGFILE)
        if not os.path.isabs(config.CACHEFILE):
            config.CACHEFILE = os.path.join(config.LOGDIR, config.CACHEFILE)
        if not os.path.isabs(config.OUTDIR):
            config.OUTDIR = addDirPrefix(config.OUTDIR)
        if not os.path.isabs(config.LIBDIR):
            config.LIBDIR = addDirPrefix(config.LIBDIR)
        config.CONFIG_FILE = path
        return config

    def show(self):
        #print(CONFIG.model_dump_json(indent=2))
        j = self.model_dump(mode='json')
        maskConfig(j)
        s = json.dumps(j, indent=2)
        print(s)

CONFIG = CONFIGCLS.load()
if CONFIG.VERBOSE > 2:
    CONFIG.show() 

if __name__ == '__main__':
    print(LLMProvider(**{'models':['1'],'base_url':'2','api_key':'sk-asdsadweweqwe'}))

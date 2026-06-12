#!/bin/python3
from collections.abc import Callable
import openai
import httpx
import json
import pyperclip
import re
import pdb
import os
import time
import inspect
from utils import *
from Config import *
from prompts import *
import checkers

def log(prompt,result):
    with open(CONFIG.LOGFILE,'a') as f:
        f.write(prompt+'\n')
        f.write('-'*50+'\n')
        f.write(result+'\n')
        f.write('='*50+'\n')

def adjustLLMParams(req:dict, model:str):
    req['model'] = model
    if model == 'o1-preview':
        req['temperature'] = 1
        msg = req['messages']
        changeSystemToUser(msg)
        req['messages'] = msg
    else:
        #req['temperature'] = 0#deterministic!
        req['temperature'] = 0.1
        req['top_p'] = 0.1
    if model == 'deepseek/deepseek-r1:free':
        req['max_tokens'] = 100000
    elif 'o1' in model:
        req['max_tokens'] = 32768
    elif '4o' in model:
        req['max_tokens'] = 16384
    elif '7B' in model:
        req['max_tokens'] = 4000
    elif model == 'Pro/deepseek-ai/DeepSeek-R1':
        req['max_tokens'] = 16384
    else:
        req['max_tokens'] = 32768
    if 'grok' not in model:
        req['presence_penalty'] = 0
        req['frequency_penalty'] = 0
    if CONFIG.DEBUG:
        print('Use LLM param:',req)
    return req

class LLMSession():
    def __init__(self, config = CONFIG, output = None, err = None):
        self.output = output
        self.err = err
        self.config = config
        self.msg:list = []
        self.providers = None
        self.client = None
        self.cache = {}
        self.secondRevise = False
        self.tokens = 0
        self.autoRevisors = {'extractNAP': self.autoReviseByLLM(napRevisor)}
        self.checkers = {'genPolicy':checkers.checkPolicy,
                         'genRRLs':checkers.checkTransitions,
                         'genFairness':checkers.checkLTL,
                         'genAP':checkers.checkProp,
                         'genInit':checkers.checkINIT}
        self.cacheFile = self.config.CACHEFILE
        self.providers = self.config.PROVIDERS
        self.strategies = self.config.STRATEGIES

    def initOpenAI(self,provider):
        openai.base_url = provider.base_url
        openai.api_key = provider.api_key
        os.environ['OPENAI_API_KEY'] = provider.api_key
        params = {'base_url':provider.base_url,
                  'api_key':provider.api_key}
        if provider.proxy:
            params['http_client'] = httpx.Client(proxy=provider.proxy)
        self.client = openai.OpenAI(**params)

    def hasCache(self)->bool:
        return os.path.exists(self.cacheFile)

    def deleteCache(self):
        return os.remove(self.cacheFile)

    def loadCache(self):
        with open(self.cacheFile,'r') as f:
            self.cache = json.load(f)

    def saveCache(self):
        with open(self.cacheFile,'w') as f:
            json.dump(self.cache,f,indent=2)

    def cacheAnswer(self,name:str,r):
        self.cache[name] = r
        self.saveCache()
  
    def clearMemory(self):
        self.msg = []

    def mountChecker(self, funcName:str, checker:Callable[[str],str|None]):
        self.checkers[funcName] = checker

    def configureParamsWithStrategy(self, req:dict, strategy:Strategy):
        provider_name, model_name = strategy.provider
        if provider_name in self.providers:
            provider = self.providers[provider_name]
            if model_name in provider.models:
                self.initOpenAI(provider)
                adjustLLMParams(req, model_name)
                return

        print('[-] Error, bad strategy in config :(!')
        exit(1)

    def dispatchRequst(self, msg:list[dict], strategy:tuple[str,str])->str|bool|dict:
        if strategy is None: strategy = self.strategies['default']
        if self.config.MODE == MODE.USEWEB:
            output = self.manualAsk(msg)
        elif self.config.MODE == MODE.USEAPI:
            output = self.callAPI(msg, strategy)
        return output

    def manualAsk(self, msg:list[dict], ifPostProcess = True)->str|bool|dict:
        self.msg = msg
        prompt = dumpMessages(msg)
        print('Ask LLM:', prompt)
        pyperclip.copy(prompt)
        answer = multiLineInput()
        if ifPostProcess:
            try:
                j = json.loads(answer)
                return self.postProcessJson(answer)
            except json.decoder.JSONDecodeError:
                return self.postProcessTxt(answer)
        else:
            return answer
        
    def callAPI(self, msg:list[dict], strategy=None)->str|bool|dict:
        self.msg = msg
        req = {'messages':msg,
               'n':self.config.N_CHOICES}

        if strategy is None: strategy = self.strategies['default']
        self.configureParamsWithStrategy(req, strategy)
        #if CONFIG.DEBUG:
        #    print(msg)
        l = []
        for i in range(self.config.TOTAL_RETRY):
            try:
                completion = self.client.chat.completions.create(**req)
            except openai.RateLimitError as e:
                if i < self.config.TIMEOUT_RETRY:
                    print(f"[-] Rate limit error, wait {(i+1)*10} seconds then try")
                    time.sleep((i + 1) * 5)
                    continue#retry
                else:
                    raise e
            except openai.APIConnectionError as e:
                if i < self.config.TIMEOUT_RETRY:
                    print(f"[-] Connection error, wait {(i+1)*10} seconds then try")
                    time.sleep((i + 1) * 5)
                    continue#retry
                else:
                    raise e
            except Exception as e:
                print(e)
                raise e

            if completion.choices is None:
                print('[-] Error')
                print(completion)
                if self.config.DEBUG and input("enter debug mode?(y/n) >").strip().lower() =='y':
                    pdb.set_trace()
                else:
                    continue#retry
            retry = False
            for choice in completion.choices:
                if choice.finish_reason == 'stop':
                    l.append(choice.message.content)
                elif choice.finish_reason == 'tool_calls':
                    l.append(choice.message.tool_calls[0].function.arguments)
                elif choice.finish_reason == 'length':
                    print('ERROR: exceed length!')
                    l.append(choice.message.content)
                    retry = True
                else:
                    print('ERROR:',choice.finish_reason)
                    print(completion)
                    print(choice)
                    if self.config.DEBUG and input("enter debug mode?(y/n) >").strip().lower() =='y':
                        pdb.set_trace()
                    else:
                        retry = True
            print('[*] Total token:',completion.usage.total_tokens)
            self.tokens += completion.usage.total_tokens
            if not retry:
                break
        if len(l) < 0:
            print('[-] Failed to get answer from LLM')
            exit(1)
        
        chooseBestAnswer = lambda l:l[0]#adhoc
        result = chooseBestAnswer(l)
        result = debugInterface(result)

        if not completion.choices[0].message.tool_calls:
            return self.postProcessTxt(result)
        else:
            return self.postProcessJson(result)
   
    def eliminateThink(self, s:str)->str:
        if '<think>' in s and '</think>' in s:
            if r := re.search(r'<think>([\S\s]+?)</think>', s):
                pos_r = r.span()[1]
                pos_l = r.span()[0]
                return s[:pos_l]+s[pos_r:]
        return s

    def postProcessTxt(self, result:str)->str|bool:
        if CONFIG.DEBUG:
            print('result',result)
        result = self.eliminateThink(result)
        if '```' in result:
            try:
                result = re.findall(r'```[^\n]*\n([^`]*)\n```', result)[0]
            except Exception as e:
                print('Error:',e)
                pdb.set_trace()
        if self.config.LOG:
            log(dumpMessages(self.msg),result)
        if result.strip().replace('\n','').replace('\r','').replace(' ','').upper() == 'OK':
            return False#indicate no error
        self.output = result.strip()
        self.msg.append(assistant(result))
        return self.output

    def postProcessJson(self,result:str)->dict:
        try:
            j = json.loads(result)
        except Exception as e:
            print(e)
            raise e
        if self.config.LOG:
            j2 = j.copy()
            if not self.config.DEBUG:
                if 'think' in j2:
                    j2.pop('think')
            log(dumpMessages(self.msg),json.dumps(j2))
        if 'think' in j:
            j.pop('think')
        self.output = j
        self.msg.append(assistant(result))
        return j

    def callAPIWithStructuredOuput(self, output_spec, msg:list[dict],strategy:Strategy)->dict:
        # TODO: configure function call in strategy
        output_spec = {
            "type": "function",
            "function": {
              "name": "output",
              "description": "output the result rigorously in a structured way",
              "strict": "true",
              "parameters": {
                "type": "object",
                "properties": {
                  "ok": {
                    "type": "bool",
                    "description": "if the result is already ok"
                   },
                  "think":{
                    "type": "string",
                    "description":"thinking progress"
                 },
                  "result": "revised",
                  "description": "revised anwser if not ok"
                },
                "required": ["ok"]
              }
            }
        }
        def adjust(req, model):
            req = adjustLLMParams(req, model)
            req['tools'] = [output_spec]
            return req
        return callAPI(msg, strategy=strategy)

    def reviseWithError1(self, err:str)->str:
        self.err = err
        ipt= f'''\
[draft]
{self.output}

[error]
{self.err}'''
        prompt = generalRevisor(ipt)
        return self.dispatchRequst(prompt, strategy = self.strategies['revise'])

    def reviseWithError2(self, err:str)->str:
        self.err = err
        ipt= f'''\
[draft]
{self.output}

[error]
{self.err}'''
        prompt = policyRevisorNew(ipt)
        return self.dispatchRequst(prompt, strategy = self.strategies['revise'])

    def reviseWithErrorDetail(self, err:str)->str:
        self.err = err
        prompt = self.msg
        if self.secondRevise:
            prompt.append(user(err))
        else:
            prompt += generalRevisorDetail(err)
            self.secondRevise = True
        return self.dispatchRequst(prompt, strategy = self.strategies['revise'])

    def autoReviseByLLM(self, revisePromptMaker:Callable[[str],list[dict]]):
        def helper(ipt:str):
            nonlocal self
            prompt = revisePromptMaker(ipt)
            return self.dispatchRequst(prompt, strategy = self.strategies['revise'])
        return helper

    def askWithErrorHandling(self, msg:list[dict], errorChecker:Callable[[str],str|None], reviseWithError:Callable[[str],str]|None = None, strategy:tuple[str,str]|None = None):
        if reviseWithError is None: reviseWithError = self.reviseWithError1
        output = self.dispatchRequst(msg, strategy = strategy)
        err = None
        n = 0
        while err := errorChecker(output):
            n += 1
            output = reviseWithError(err)
            if n > self.config.ERROR_RETRY:
                break
        return output

    def askWithLLMCheckRevise(self, msg:list[dict], revisor:Callable[[str],str|None],strategy:tuple[str,str]|None = None):
        return self.askWithErrorHandling(msg,revisor,lambda x:x, strategy)

    def generalAskWithAutoCheck(self,name:str,prompt:list[dict], strategy:tuple[str,str]|None = None)->str:
        #automatically chooce cache and strategy 
        if name in self.cache: return self.cache[name]
        if name == 'genPolicy':
            revisor = self.reviseWithErrorDetail
        else:
            revisor = self.reviseWithError1
        if not strategy:
            if name in self.strategies:
                strategy = self.strategies[name]
            else:
                strategy = self.strategies['default']
        if name in self.checkers:
            r = self.askWithErrorHandling(prompt, errorChecker = self.checkers[name], reviseWithError = revisor, strategy=strategy)
        elif name in self.autoRevisors:
            r = self.askWithLLMCheckRevise(prompt, self.autoRevisors[name], strategy = strategy)
        else:
            r =  self.dispatchRequst(prompt,strategy=strategy)

        self.cacheAnswer(name,r)
        return r

    def splitPolicy(self,protocol_desc:str)->tuple[str,str,str,str]:
        #add init to state changes version
        #return EQdes,RRLdes,initial state,property
        # TODO: separate threat model to another file
        name = inspect.currentframe().f_code.co_name
        if name in self.cache: return self.cache[name]
        threatModel = protocol_desc.split('\n\n')[-1]
        txt = protocol_desc.replace(threatModel,'')
        combine = lambda i,s : f'[Initial States]\n{i}\n[State Changes]\n{s}\n'
        if r := preprocess(txt):
            answer = combine(r[0],r[1]),r[2],r[0],threatModel
        else:
            prompt = splitPromptTemplate(txt)
            txt = self.dispatchRequst(prompt, strategy = self.strategies['preprocess'])
            print('*',txt)
            if r := preprocess(txt):
                answer = combine(r[0],r[1]),r[2],r[0],threatModel
            else:
                print('[-] Error, r=', r)
                pdb.set_trace()
            if threatModel == '':
                print('[-] Error when spliting policy, there are no properties! Please check the input format.')
                exit(1)
        self.cacheAnswer(name, answer)
        return answer

    def splitPolicyBak(self,protocol_desc:str)->tuple[str,str,str,str]:
        #return EQdes,RRLdes,initial state,property
        # TODO: separate threat model to another file
        name = inspect.currentframe().f_code.co_name
        if name in self.cache: return self.cache[name]
        threatModel = protocol_desc.split('\n\n')[-1]
        txt = protocol_desc.replace(threatModel,'')
        if r := preprocess(txt):
            answer = r[1],r[2],r[0],threatModel
        else:
            prompt = splitPromptTemplate(txt)
            txt = self.dispatchRequst(prompt, strategy = self.strategies['preprocess'])
            print('*',txt)
            if r := preprocess(txt):
                answer = r[1],r[2],r[0],threatModel
            else:
                print('[-] Error, r=', r)
                pdb.set_trace()
        self.cacheAnswer(name, answer)
        return answer

    def genPolicy(self, protocol_desc:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = generatePolicy(protocol_desc)
        return self.generalAskWithAutoCheck(name, prompt)

    def genEvents(self, policy:str, description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = eventsPromptTemplate(policy, description)
        return self.generalAskWithAutoCheck(name, prompt)

    def filterEvents(self,events:str, description:str)->list:
        name = inspect.currentframe().f_code.co_name
        prompt = filterPromptTemplate(events,description)
        return eval(self.generalAskWithAutoCheck(name, prompt))#INSECURE

    def genPolicyVars(self, desc:str, formal:str, variables:list)->dict[str,str]:
        name = inspect.currentframe().f_code.co_name
        prompt = policyVarsPromptTemplate(desc, formal, variables)
        return dict(eval(self.generalAskWithAutoCheck(name, prompt)))

    def genEventVars(self, desc:str, formal:str, variables:list)->dict[str,str]:
        name = inspect.currentframe().f_code.co_name
        prompt = eventVarsPromptTemplate(desc, formal, variables)
        return dict(eval(self.generalAskWithAutoCheck(name, prompt)))

    def genPropVars(self, desc:str, formal:str, variables:list)->dict[str,str]:
        name = inspect.currentframe().f_code.co_name
        prompt = propVarsPromptTemplate(desc, formal, variables)
        return dict(eval(self.generalAskWithAutoCheck(name, prompt)))

    def genFairness(self,ap:str,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = fairnessPromptTemplate(ap,description)
        return self.generalAskWithAutoCheck(name, prompt)

    def genInit(self, init_template:str, init_desc:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = initPromptTemplate(init_template,init_desc)
        return self.generalAskWithAutoCheck(name, prompt)

    def genRRLs(self,state_template:str, events:str, description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = RRLsPromptTemplate(state_template, events, description)
        return self.generalAskWithAutoCheck(name, prompt)

    def extractNAP(self,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = napPromptTemplate(description)
        return self.generalAskWithAutoCheck(name, prompt)

    def genAP(self,state_template:str,events:str,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = apPromptTemplate(state_template, events, description)
        return self.generalAskWithAutoCheck(name, prompt)

    #def chooseFixAttributes(self, choices:list[str])->int:
    #    name = inspect.currentframe().f_code.co_name
    #    prompt = policyReviseAttributes(self.protocol, choices)
    #    return eval(self.generalAskWithAutoCheck(name, prompt , strategy = self.strategies['revise']))
         

def preprocess(protocol_desc):
    regexp = r'\[[\w\s\(\))]*\]([\S\s]+?)\[[\w\s\(\))]*\]([\S\s]+?)\[[\w\s\(\))]*\]([\S\s]+?)$'
    if r := re.findall(regexp,protocol_desc):
        return r[0]

def debugInterface(txt):
    if CONFIG.VERBOSE > 1:
        print('-'*50)
        print(txt)
        print('='*50)
    if CONFIG.DEBUG:
        cmd = input('[debug] press enter to continue>').strip()
        if cmd == 'e':
            txt = editInTmpFile(txt)
        elif cmd == 'q':
            exit(1)
        else:
            pass
    return txt

def listModels():
    print(openai.models.list())

def singleQuestion():
    CONFIG.DEBUG = True
    CONFIG.LOG = False
    print('Ask LLM by API:')
    txt = multiLineInput()
    prompt = [system(txt)]
    llm = LLMSession()
    print('----output------')
    print(llm.dispatchRequst(prompt, strategy = CONFIG.STRATEGIES['gen']))


if __name__ == '__main__':
    singleQuestion()
    #print(debug1())
    #listModels()
    #print(debug1())
    #test4()

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
import ast as python_ast
import hashlib
from copy import deepcopy
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
    def __init__(self, config = CONFIG, output = None, err = None, context_id=None):
        self.output = output
        self.err = err
        self.config = config
        self.msg:list = []
        self.providers = None
        self.client = None
        self.cache = {}
        self.secondRevise = False
        self.tokens = 0
        self.context_id = context_id
        self.source_context = ''
        self.stage_records = []
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
                  'api_key':provider.api_key,
                  'timeout': self.config.REQUEST_TIMEOUT,
                  'max_retries': 0}
        if provider.proxy:
            params['http_client'] = httpx.Client(proxy=provider.proxy)
        self.client = openai.OpenAI(**params)

    def hasCache(self)->bool:
        return os.path.exists(self.cacheFile)

    def deleteCache(self):
        if os.path.exists(self.cacheFile):
            os.remove(self.cacheFile)

    def loadCache(self):
        with open(self.cacheFile,'r') as f:
            saved = json.load(f)
        if saved.get('schema_version') != 2 or saved.get('context_id') != self.context_id:
            raise ValueError('Cache does not match this input, configuration, and pipeline version. Use a new output directory.')
        self.cache = saved['answers']
        self.stage_records = saved.get('stages', [])

    def saveCache(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.cacheFile)), exist_ok=True)
        temporary = self.cacheFile + '.tmp'
        with open(temporary,'w') as f:
            json.dump({'schema_version': 2, 'context_id': self.context_id,
                       'answers': self.cache, 'stages': self.stage_records},f,indent=2)
        os.replace(temporary, self.cacheFile)

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
        completion = None
        for i in range(self.config.TOTAL_RETRY):
            l = []
            try:
                completion = self.client.chat.completions.create(**req)
            except openai.RateLimitError as e:
                if i < self.config.TIMEOUT_RETRY:
                    print(f"[-] Rate limit error, wait {(i+1)*10} seconds then try")
                    time.sleep((i + 1) * 5)
                    continue#retry
                else:
                    raise e
            except (openai.APIConnectionError, openai.APITimeoutError) as e:
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
            l = []
            for choice in completion.choices:
                if choice.finish_reason == 'stop':
                    l.append(choice.message.content)
                elif choice.finish_reason == 'tool_calls':
                    l.append(choice.message.tool_calls[0].function.arguments)
                elif choice.finish_reason == 'length':
                    print('ERROR: exceed length!')
                    retry = True
                else:
                    print('ERROR:',choice.finish_reason)
                    print(completion)
                    print(choice)
                    if self.config.DEBUG and input("enter debug mode?(y/n) >").strip().lower() =='y':
                        pdb.set_trace()
                    else:
                        retry = True
            usage = completion.usage.total_tokens if completion.usage else 0
            print('[*] Total token:',usage)
            self.tokens += usage
            if not retry:
                break
        if not l:
            raise RuntimeError('No complete LLM response was received; no partial answer was cached.')
        
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
            blocks = re.findall(r'```[^\n]*\n(.*?)```', result, re.S)
            if len(blocks) != 1:
                raise ValueError('Expected exactly one complete output code block.')
            result = blocks[0]
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
        self.secondRevise = False
        output = self.dispatchRequst(msg, strategy = strategy)
        for n in range(self.config.ERROR_RETRY + 1):
            err = errorChecker(output)
            self.stage_records.append({'attempt': n, 'output': output, 'error': err})
            self.saveCache()
            if not err:
                return output
            if n == self.config.ERROR_RETRY:
                raise ValueError(f'Validation failed after {n} repairs: {err}')
            self.output = output
            output = reviseWithError(err)

    def askWithLLMCheckRevise(self, msg:list[dict], revisor:Callable[[str],str|None],strategy:tuple[str,str]|None = None):
        return self.askWithErrorHandling(msg,revisor,lambda x:x, strategy)

    def generalAskWithAutoCheck(self,name:str,prompt:list[dict], strategy:tuple[str,str]|None = None)->str:
        #automatically chooce cache and strategy 
        prompt = deepcopy(prompt)
        if self.source_context and not any(self.source_context in m['content'] for m in prompt):
            prompt.append(user('[Original protocol input: preserve these facts during generation and repair]\n' + self.source_context))
        if name == 'genPolicy':
            revisor = self.reviseWithErrorDetail
        else:
            revisor = self.reviseWithErrorDetail
        if not strategy:
            if name in self.strategies:
                strategy = self.strategies[name]
            else:
                strategy = self.strategies['default']
        cache_key = name + ':' + hashlib.sha256(json.dumps([prompt, strategy.model_dump()],sort_keys=True).encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]
        self.stage_records.append({'stage': name, 'prompt_hash': cache_key})
        if name in self.checkers:
            r = self.askWithErrorHandling(prompt, errorChecker = self.checkers[name], reviseWithError = revisor, strategy=strategy)
        elif name in self.autoRevisors:
            r = self.askWithLLMCheckRevise(prompt, self.autoRevisors[name], strategy = strategy)
        else:
            r =  self.dispatchRequst(prompt,strategy=strategy)

        self.cacheAnswer(cache_key,r)
        return r

    def genPolicy(self, protocol_desc:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = generatePolicy(protocol_desc)
        return self.generalAskWithAutoCheck(name, prompt)

    def genEvents(self, policy:str, description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = eventsPromptTemplate(policy, description)
        return self.generalAskWithAutoCheck(name, prompt)

    def filterEvents(self, events: str, description: str) -> list:
        count = len(events.splitlines())
        def validate(answer):
            try:
                ids = python_ast.literal_eval(answer)
                if not isinstance(ids, list) or not ids:
                    return 'Return a nonempty Python list of 1-based event IDs.'
                if any(type(i) is not int or not 1 <= i <= count for i in ids):
                    return f'Each event ID must be an integer between 1 and {count}.'
            except (ValueError, SyntaxError, TypeError):
                return 'Return only a Python list of integer event IDs.'
            return None
        self.checkers['filterEvents'] = validate
        result = self.generalAskWithAutoCheck('filterEvents', filterPromptTemplate(events, description))
        return python_ast.literal_eval(result)

    def _variableTypes(self, name, prompt, variables):
        allowed = {'User', 'Device', 'Server', 'Client', 'App', 'Principal', 'Cloud',
                   'Nat', 'Qid', 'Set', 'List', 'Item', 'Bool', 'Action', 'Arguments', 'Attributes', 'Key'}
        def validate(answer):
            try:
                pairs = python_ast.literal_eval(answer)
                mapping = dict(pairs)
                if set(mapping) != set(variables):
                    return f'Return exactly these variable names: {variables}.'
                if any(t not in allowed for t in mapping.values()):
                    return f'Use only these existing sorts: {sorted(allowed)}.'
            except (ValueError, SyntaxError, TypeError):
                return 'Return a Python dictionary or list of (variable, sort) pairs.'
            return None
        self.checkers[name] = validate
        result = self.generalAskWithAutoCheck(name, prompt)
        return dict(python_ast.literal_eval(result))

    def genPolicyVars(self, desc, formal, variables):
        return self._variableTypes('genPolicyVars', policyVarsPromptTemplate(desc, formal, variables), variables)

    def genEventVars(self, desc, formal, variables):
        return self._variableTypes('genEventVars', eventVarsPromptTemplate(desc, formal, variables), variables)

    def genPropVars(self, desc, formal, variables):
        return self._variableTypes('genPropVars', propVarsPromptTemplate(desc, formal, variables), variables)

    def genFairness(self,ap:str,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = fairnessPromptTemplate(ap,description)
        return self.generalAskWithAutoCheck(name, prompt)

    def genInit(self, init_template:str, init_desc:str, threat:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = initPromptTemplate(init_template,init_desc,threat)
        return self.generalAskWithAutoCheck(name, prompt)

    def genRRLs(self,state_template:str, events:str, description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = RRLsPromptTemplate(state_template, events, description)
        return self.generalAskWithAutoCheck(name, prompt)

    def extractNAP(self,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = napPromptTemplate(description)
        return self.generalAskWithAutoCheck(name, prompt)

    def genSlots(self, template:str, init:str, rules:str, roles:str, slots:dict[str,str])->str:
        self.mountChecker('genSlots', checkers.slots(list(slots), template + '\n' + init + '\n' + rules))
        slotText = '\n'.join(f'{name} : {description}' for name, description in slots.items())
        return self.generalAskWithAutoCheck('genSlots', slotsPromptTemplate(template, init, rules, roles, slotText))

    def genAP(self,state_template:str,events:str,description:str)->str:
        name = inspect.currentframe().f_code.co_name
        prompt = apPromptTemplate(state_template, events, description)
        return self.generalAskWithAutoCheck(name, prompt)

    #def chooseFixAttributes(self, choices:list[str])->int:
    #    name = inspect.currentframe().f_code.co_name
    #    prompt = policyReviseAttributes(self.protocol, choices)
    #    return eval(self.generalAskWithAutoCheck(name, prompt , strategy = self.strategies['revise']))
         

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

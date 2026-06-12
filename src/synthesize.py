#!/bin/python3
from LLMInterface import *
from calculateInitState import calculateInitState
from AST import *
from utils import disDuplicate
from analyze import extractEventsFromAST, extractVarsFromAST, toVarTypeDecls, giveEvtDecls
from transformAST import transformStateRule, transformEventRule, transformProposition, transformInit, addVarTypes
from Config import CONFIG

genRules = lambda init,varTypeDecls,policy,varTypeDecls2,evtTypeDecls,events,transitionRules:f'''\
load ../lib/Iot .
mod SYSTEM is
protecting Iot .
eq init = idle @ {init} .

vars .. ... .... ..... ...... ....... : Set .

*** variables
{varTypeDecls}
*** policy
{policy}
endm

mod TRANSITION is
including SYSTEM .
var E : Event .
var S : Soup .
vars .. ... .... ..... ...... ....... : Set .
{varTypeDecls2}
*** events type declaration
{evtTypeDecls}
*** events
{events}
*** transitions
{transitionRules}

endm
'''

timePassRuleStr = '''
rl [rtp]: E @ S < system | ('time' : N , .. ) >
=> ep: timepass @ S < system | ('time' : (N + 1) , .. ) > .
'''

def genPropType(ap_desc):
    l = ['ops']
    for line in ap_desc.strip().split('\n'):
        pn = line.split(':')[0]
        l.append(pn)
    l += [':','->','Prop','.']
    return ' '.join(l)

genCheckers = lambda varTypeDecls,propType,prop_explain, propositions,fairness:f'''\
load rules .
load model-checker .
mod PREDS is
pr TRANSITION * (sort State to State') .
including SATISFACTION .
pr BOOL-OPS .

subsort Vertex < State .

{varTypeDecls}
var Vtx : Vertex .
var P : Prop .
var E : Event .
var S : Soup .
vars .. ... .... ..... ...... ....... : Set .

ops boundReached sp : -> Prop .
*** generated type declarations
{propType}

*** proposition comment
{prop_explain}

*** generated propositions
{propositions}

*** predefined
ceq E @ S  |= sp = true if subject(E) == system . *** system performs actions
ceq E @ S < system | 'counter' : N , ... >  |= boundReached = true if N >= 5 . *** Max turns number
ceq E @ S < system | 'time' : N , ... >  |= boundReached = true if N >= 3 . *** time pass

eq Vtx |= P = false [owise] .

endm

mod CHECK is
pr PREDS .
including MODEL-CHECKER .

ops spec basic fairness : -> Prop .

eq basic = [] (~ boundReached /\ ~ sp) .

eq fairness = 
{fairness} .

*** security property specification
eq spec = O ~ (fairness /\\ basic) .
endm

load ../lib/postProcess .
'''

def extractAndNameVariables(genVarFunc, desc, formal_str, ast, vtypes:dict = {})->tuple[dict,str]:
    print('[*] Extract variables')
    variables2 = extractVarsFromAST(ast)
    variables = list(vtypes.keys())
    variables_delta = list(set(variables2) - set(variables))
    if variables_delta:
        print('[*] Find unresolved variables')
        print('[*] Generating variable types with LLM...')
        vtypes_delta = genVarFunc(desc, formal_str, variables_delta)
        print(vtypes_delta)
        vtypes.update(vtypes_delta)
    print('[*] Add varable types to AST')
    addVarTypes(ast, vtypes)
    varTypeDecls = toVarTypeDecls(vtypes)
    return vtypes,varTypeDecls
def synthesizeRules(llm, EQ_desc, RRL_desc, init_desc):
    #protocol = multiLineInput('Please input protocol description:')
    print('[*] Generating policy with LLM...')
    #print('Do you want to exit now?')
    policy = llm.genPolicy(EQ_desc)
    ast = parseAST(policy)
    
    print('[*] Extract state rules variables')
    defaultVtypes = {'N':'Nat'}    

    vtypes,varTypeDecls = extractAndNameVariables(llm.genPolicyVars, EQ_desc, policy, ast, defaultVtypes)

    print('[*] Calculating init state...')
    state_template = calculateInitState(ast,vtypes)
    print('[+] The init state template:')
    print(state_template)

    print('[*] Transform state rule AST to repair wellformedness...')
    hasFresh, hasCurrentTime = transformStateRule(ast)
    print('hasFresh',hasFresh,'hasCurrentTime',hasCurrentTime)
    policy = str(ast)
    print(policy)

    evts_AST:list[EVENT] = extractEventsFromAST(ast)
    eventsList = '\n'.join([str(evt_AST) for evt_AST in evts_AST])
    print(eventsList)#
    eids = llm.filterEvents(eventsList, RRL_desc)
    eids = disDuplicate(eids)

    print(eids)
    print([evts_AST[eid-1] for eid in eids])#
    eventDecls = giveEvtDecls([evts_AST[eid-1] for eid in eids])
    print(eventDecls)

    print('[*] Calculating event type...')
    vtypes.update({'MessageA':'Qid'})
    evtTypes = '\n'.join([e.typeDecl(vtypes) for e in eventDecls])
    eventDecls = '\n'.join([str(e) for e in eventDecls])
    
    print('[*] Generating init state with LLM...')
    init = llm.genInit(state_template,init_desc)
    init_ast = parseInitAST(init)
    transformInit(init_ast, hasFresh, hasCurrentTime)
    init = str(init_ast)
    print(init)

    print('[*] Generating event rules with LLM...')
    transitionRules = llm.genRRLs(str(state_template),eventDecls,RRL_desc)
    print(transitionRules)

    print('[*] Transform event rules AST...')
    ast2 = parseAST(transitionRules)

    vtypes2,varTypeDecls2 = extractAndNameVariables(llm.genEventVars,RRL_desc, transitionRules, ast2, vtypes)

    transformEventRule(ast2)
    transitionRules = str(ast2)
    if hasCurrentTime:
        transitionRules += timePassRuleStr
    print(transitionRules)

    rules = genRules(init,varTypeDecls,policy,varTypeDecls2,evtTypes,eventDecls,transitionRules)

    #return rules, state_template, eventDecls
    return rules, state_template, eventsList

def synthesizeChecker(llm,property_desc:str,state_template:str,events:str):
    print('[*] Generating natural language description of propositions with LLM...')
    ap_desc = llm.extractNAP(property_desc)
    print(ap_desc)
    prop_explain = '\n'.join(['*** '+line for line in ap_desc.split('\n')])
    #print(prop_explain)

    print('[*] Generating atomic proposition definitions with LLM...')
    proposition = llm.genAP(state_template,events,ap_desc)
    ast = parseAST(proposition)
    defaultVtypes = {'N':'Nat', 'Act':'Action', 'PrincipalA':'Principal' , 'Message':'Qid'}

    vtypes,varTypeDecls = extractAndNameVariables(llm.genPropVars,ap_desc, proposition, ast, defaultVtypes)
    proposition = str(transformProposition(ast))
    print(proposition)

    print('[*] Generating property with LLM...')
    fairness = llm.genFairness(ap_desc,property_desc)
    print(fairness)

    checker = genCheckers(varTypeDecls,genPropType(ap_desc),prop_explain, proposition, fairness)
    return checker

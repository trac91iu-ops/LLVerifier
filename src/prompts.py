#!/bin/python3
from prompts_text import *

LLMMSG = lambda role,c:{'role': role, 'content': c}
system = lambda c:LLMMSG('system',c)
assistant = lambda c:LLMMSG('assistant',c)
user = lambda c:LLMMSG('user',c)
tool = lambda c:LLMMSG('tool',c)

def genConversation(system_setting,trainings=[]):
    c = []#conversertion list
    c.append(system(system_setting))
    for q,a in trainings:
        c.append(user(q))
        c.append(assistant(a))
    return lambda ipt:c+[user(ipt)]

def dumpMessages(msg):
    if type(msg) == str:
        return str
    return ''.join([f"---{m['role']}---\n"+m['content'] for m in msg])

def changeSystemToUser(msg):
    for m in msg:
        if m['role'] == 'system':
            m['role'] = 'user'
    return msg

    
def generatePolicy(ipt):
    trainings = [(policy_shot_q1, policy_shot_a1),
                 (policy_shot_q2, policy_shot_a2)]
    return (genConversation(policy_system,trainings))(ipt)

def eventsPromptTemplate(protocol,description):
    ipt= f'''\
[protocol]
{protocol}
[description]
{description}'''
    trainings = [(event_shot_q1,event_shot_a1)]
    return (genConversation(event_system,trainings))(ipt)

def policyVarsPromptTemplateOld(ipt):
    #DEPRECATED
    trainings = [(vars_shot_q1,vars_shot_a1)]
    return (genConversation(vars_systemBak,trainings))(ipt)

def policyVarsPromptTemplate(protocol,formal,variables):
    trainings = [(policy_vars_shot_q1,policy_vars_shot_a1)]
    ipt= f'''\
[protocol]
{protocol}

[formal]
{formal}

[variables]
{variables}\
    '''
    return (genConversation(policy_vars_system,trainings))(ipt)

def eventVarsPromptTemplate(protocol,formal,variables):
    trainings = [(event_vars_shot_q1,event_vars_shot_a1)]
    ipt= f'''\
[protocol]
{protocol}

[formal]
{formal}

[variables]
{variables}\
    '''
    return (genConversation(event_vars_system,trainings))(ipt)

def propVarsPromptTemplate(protocol,formal,variables):
    trainings = [(prop_vars_shot_q1,prop_vars_shot_a1)]
    ipt= f'''\
[protocol]
{protocol}

[formal]
{formal}

[variables]
{variables}\
    '''
    return (genConversation(prop_vars_system,trainings))(ipt)

def fairnessPromptTemplate(ipt1,ipt2):
    ipt= f'''\
[Atomic propositions]
{ipt1}

[description]
{ipt2}\
    '''
    trainings = [(fairness_shot_q1,fairness_shot_a1)]
    return (genConversation(fairness_system,trainings))(ipt)

def initPromptTemplate(ipt1,ipt2):
    ipt = f'''\
[template]
{ipt1}

[description]
{ipt2}\
    '''
    trainings = [(init_shot_q1,init_shot_a1),
                 (init_shot_q2,init_shot_a2)]
    return (genConversation(init_system,trainings))(ipt)

def RRLsPromptTemplate(ipt1,ipt2,ipt3):
    ipt = f'''\
[state template]
{ipt1}

[events]
{ipt2}

[description]
{ipt3}\
    '''
    trainings = [(rrls_shot_q1,rrls_shot_a1),
                 (rrls_shot_q2,rrls_shot_a2)]
    return (genConversation(rrls_system,trainings))(ipt)

def apPromptTemplate(ipt1,ipt2,ipt3):
    ipt = f'''\
[state template]
{ipt1}

[events]
{ipt2}

[description]
{ipt3}'''
    #trainings = [(ap_shot_q1,ap_shot_a1)]
    #return (genConversation(ap_system,trainings))(ipt)
    trainings = [(ap_shot_q1New,ap_shot_a1New)]
    return (genConversation(ap_systemNew,trainings))(ipt)


def napPromptTemplate(ipt):
    trainings = [(nap_shot_q1,nap_shot_a1)]
    return (genConversation(nap_system,trainings))(ipt)

def splitPromptTemplate(ipt):
    trainings = [(split_shot_q1,split_shot_a1)]
    return (genConversation(split_system,trainings))(ipt)

def filterPromptTemplate(ipt1,ipt2):
    ipt = f'''\
[events]
{ipt1}

[description]
{ipt2}'''   
    trainings = [(filter_shot_q1,filter_shot_a1)]
    return (genConversation(filter_system,trainings))(ipt)

def baselinePrompt(ipt):
    return genConversation(genMaudeSystem)(ipt)

def generalRevisor(ipt):
    return genConversation(general_revisor_system)(ipt)

def generalRevisorDetail(ipt):
    return genConversation(detail_revisor_system)(ipt)

def policyRevisorNew(ipt):
    return genConversation(policy_revisor_system)(ipt)

def napRevisor(ipt):
    trainings = [(nap_revisor_q1,nap_revisor_a1),
                 (nap_revisor_q2,nap_revisor_a2),
                 (nap_revisor_q3,nap_revisor_a3)
                 ]
    return (genConversation(nap_revisor_system, trainings))(ipt)

###NO USED in current version
def policyReviseAttributes(protocol:str, choices:list[str]):
    cl = ''
    for i,choice in enumerate(choices):
        cl += f'Choice{i}: ' + choice + '\n'

    ipt=f'''\
[protocol]
{protocol}

[choices list]
{cl}\
    '''
    trainings:list[tuple[str,str]] = []
    return genConversation(choose_missing_attributes_system, trainings)(ipt)

###DEPRECATED
def policyRevisor(ipt):
    #DEPRECATED
    trainings = [(revisor_shot_q1,revisor_shot_a1),
                 (revisor_shot_q2,revisor_shot_a2),
                 (revisor_shot_q3,revisor_shot_a3),
                 (revisor_shot_q4,revisor_shot_a4),
                 (revisor_shot_q5,revisor_shot_a5)
                 ]
    return (genConversation(revisor_system,trainings))(ipt)

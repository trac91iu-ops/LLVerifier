#!/bin/python3
"""Predefined security-property templates for checker.maude.

Three families:
  OWN : the attacker gains an authority G while condition C holds across the step
        <> (C /\\ [P] /\\ ~ G /\\ O (C /\\ G))
  CTRL: the device is switched on although the actor stays unauthorized
        <> (~ deviceOn /\\ ~ A /\\ O ([E] /\\ deviceOn /\\ ~ A))
  CTX : (AI agent protocols, A2A) the isolation of a conversation context between clients breaks:
        the attacker reads the victim's data R or tampers with the victim's context T
        <> (R \\/ T)
Each subtype names the slots it needs. State slots are filled with Maude state
patterns (e.g. "< cloudA | (deviceB : ('owner' : userC , ..) , ...) >"); the event
slot `attackerActs` is generated from the attacker role.
"""

SUBTYPES = {
    'OWN-remote': {
        'slots': {'attackerLocal': 'the attacker is near / local to the device',
                  'attackerOwner': 'the attacker is recorded as an owner of the device'},
        'optional': {'victimOwner': 'the victim is recorded as the owner of the device'},
        'safety': '<> (~ attackerLocal /\\ {P}~ attackerOwner /\\ O (~ attackerLocal /\\ attackerOwner))',
    },
    'OWN-stealth': {
        'slots': {'deviceTrustsAttacker': 'the device trusts the attacker',
                  'cloudRecordsTrust': "the cloud records the device's trust in the attacker"},
        'optional': {},
        'safety': '<> (~ cloudRecordsTrust /\\ ~ deviceTrustsAttacker /\\ O (~ cloudRecordsTrust /\\ deviceTrustsAttacker))',
    },
    'CTRL-direct': {
        'slots': {'deviceOn': 'the device is on',
                  'attackerAuthorized': 'the cloud records the attacker as authorized for the device (e.g. associated with it, or in its trusted set)'},
        'optional': {},
        'event': True,
        'safety': '<> (~ deviceOn /\\ ~ attackerAuthorized /\\ O (attackerActs /\\ deviceOn /\\ ~ attackerAuthorized))',
    },
    'CTRL-revoked': {
        'slots': {'deviceOn': 'the device is on',
                  'attackerAuthorized': 'the cloud records that the (revoked) actor still holds a permission for the device'},
        'optional': {},
        'safety': '<> (~ deviceOn /\\ ~ attackerAuthorized /\\ O (deviceOn /\\ ~ attackerAuthorized))',
    },
    'CTX-isolation': {
        'slots': {'attackerReadsVictimData': 'the attacker holds a message that the victim sent',
                  'victimContextTampered': "the victim's context holds a message that the attacker sent"},
        'optional': {},
        'safety': '<> (attackerReadsVictimData \\/ victimContextTampered)',
    },
}


def safetyFormula(subtype: str, slots: dict[str, str]) -> str:
    t = SUBTYPES[subtype]
    P = ''.join(f'{name} /\\ ' for name in t['optional'] if name in slots)
    return t['safety'].replace('{P}', P)


def renderChecker(subtype: str, slots: dict[str, str], attacker: str = 'userC',
                  varDecls: str = '', forbidSystemEvents: bool = False) -> str:
    """slots: slot name -> Maude state pattern (internal states) for which the slot holds."""
    t = SUBTYPES[subtype]
    missing = set(t['slots']) - set(slots)
    if missing:
        raise ValueError(f'{subtype} needs slots {sorted(missing)}')
    names = [n for n in list(t['slots']) + list(t['optional']) if n in slots]
    if t.get('event'):
        names.append('attackerActs')
    descr = {**t['slots'], **t['optional'], 'attackerActs': f'{attacker} performs an action'}
    props = [f'eq E @ S {slots[n]} |= {n} = true .' for n in names if n != 'attackerActs']
    if t.get('event'):
        props.append(f'ceq E @ S |= attackerActs = true if subject(E) == {attacker} .')
    basic = '[] (~ boundReached /\\ ~ sp)' if forbidSystemEvents else '[] (~ boundReached)'
    return f'''\
load rules .
load model-checker .
mod PREDS is
pr TRANSITION * (sort State to State') .
including SATISFACTION .
pr BOOL-OPS .

subsort Vertex < State .

vars N : Nat .
{varDecls}
var Vtx : Vertex .
var P : Prop .
var E : Event .
var S : Soup .
vars .. ... .... ..... ...... ....... : Set .

ops boundReached sp : -> Prop .
ops {' '.join(names)} : -> Prop .

*** property template: {subtype} (attacker = {attacker})
{chr(10).join(f'*** {n} : {descr[n]}' for n in names)}

{chr(10).join(props)}

*** predefined
ceq E @ S |= sp = true if subject(E) == system . *** system performs actions
ceq E @ S < system | 'counter' : N , ... > |= boundReached = true if N >= 5 . *** Max turns number
ceq E @ S < system | 'time' : N , ... > |= boundReached = true if N >= 3 . *** time pass

eq Vtx |= P = false [owise] .
endm

mod CHECK is
pr PREDS .
including MODEL-CHECKER .

ops spec basic safety : -> Prop .

eq basic = {basic} .

eq safety = {safetyFormula(subtype, slots)} .

*** security property specification
eq spec = O ~ (safety /\\ basic) .
endm

load ../lib/postProcess .
'''

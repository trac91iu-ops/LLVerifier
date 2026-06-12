#!/bin/python3
from AST import *
from DSLSyntax import PrinTypes
from utils import allf
from copy import deepcopy
from LLMInterface import LLMSession
from exceptions import *

class astTransformer(ASTVisitor):
    def __init__(self):
        super().__init__()
    def matchVar(x): return type(x) == VARIABLE
    def matchInt(x): return type(x) == INTEGER
    def matchSet(x): return type(x) == SET
    def matchDots(x): return type(x) == DOTS
    def matchFresh(v): return v.ident.startswith('Fresh')
    def matchCTime(v): return v.ident.startswith('CurrentTime')
    def randomStr(v):#VARIABLE
        if v.ident.startswith('Fresh'):
            i = v.ident[len('Fresh'):] 
            return FUNCALL('randomStr', [QID(f"'{i}'"), VARIABLE('N','Nat')])
        return v
    def matchTest(x): return type(x) == SET
    def transformTest(x): 
        #test
        print('*',x,type(x),x.v,type(x.v))
        return SET(('BOOM'))

class dotsDisduper(astTransformer):
    def visitInState(self, istate, last):
        #propotision.constraint
        T = astTransformer
        def helper(s:SET):
            n = 0
            for i in s.v:
                if isinstance(i, DOTS):
                    n += 1
                    if n == 2:
                        s.removeOnce(i)
            return s
        istate.visit([(T.matchSet, helper)])

class dotsAdder(astTransformer):
    def visitInState(self, istate, last):
        istate.constructIndex()
        T = astTransformer
        def helper(s:SET):
            if isinstance(s.parent,SET):
                return s
            for i in s.v:
                if isinstance(i, VARIABLE):
                    if i.type_ == 'Set':
                        return s
            if len(s.v) == 1 and type(s.v[0]) != PAIR:
                return s
            if not s.has(DOTS()):
                s.add(DOTS())
            return s
        istate.visit([(T.matchSet, helper)])

class dotsAdder2(astTransformer):
    def visitInState(self, istate, last):
        istate.constructIndex()
        T = astTransformer
        def helper(s:SET):
            if isinstance(s.parent,SET):
                return s
            for i in s.v:
                if isinstance(i, VARIABLE):
                    if i.type_ == 'Set':
                        return s
            # TODO: ap7 =| < cloudA | (deviceB : ('owner' : userC , ..) , ...) > . => < cloudA | (deviceB : ('owner' : (userC , ....) , ..) , ...) >
            if not s.has(DOTS()):
                s.add(DOTS())
            return s
        istate.visit([(T.matchSet, helper)])

class dotsFixer(astTransformer):
    def sig(self, v:DOTS)->tuple:
            l = []
            for p in v.bloodline():
                if isinstance(p, SET):
                    continue
                    #print(1,p.keys())
                    #l.append(tuple(p.keys()))
                elif isinstance(p, INTERNAL_STATE):
                    l.append(p.principal)
                elif isinstance(p, PAIR):
                    l.append(p.k)
                else:
                    l.append(p)
            return tuple(l)

    def visitStateRule(self,rule):
        T = astTransformer
        bloodchainDotsNum  = {}
        dots_num = DOTS.init_num
        rule.constructIndex()
        for is_or_e in rule.lhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                def helper(v:DOTS):
                    nonlocal dots_num
                    bloodchainDotsNum[self.sig(v)] = dots_num
                    v.dots_num = dots_num
                    dots_num += 1
                    return v
                istate.visit([(T.matchDots, helper)])
        #print(bloodchainDotsNum)
        for is_or_e in rule.rhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                def helper2(v:DOTS):
                    if self.sig(v) in bloodchainDotsNum:
                        n = bloodchainDotsNum[self.sig(v)]
                        v.dots_num = n
                    return v
                istate.visit([(T.matchDots, helper2)])

    def visitEventRule(self,rule):
        dots_num = DOTS.init_num
        rule.constructIndex()
        T = astTransformer
        for istate in rule.lhs:
            def helper(v:DOTS):
                nonlocal dots_num
                v.dots_num = dots_num
                dots_num += 1
                return v
            istate.visit([(T.matchDots, helper)])

    def visitProposition(self, prop):
        dots_num = DOTS.init_num
        prop.constructIndex()
        T = astTransformer
        if isinstance(prop.constraint, INTERNAL_STATE):
            istate = prop.constraint
            def helper(v:DOTS):
                nonlocal dots_num
                v.dots_num = dots_num
                dots_num += 1
                return v
            istate.visit([(T.matchDots, helper)])

class dotsRemover(astTransformer):
    def visitSet(self, s:SET):
        if s.hasType(DOTS):
            s.removeByType(DOTS)
        for i in s.v:
            if isinstance(i, PAIR):
                if isinstance(i.v, SET):
                    self.visitSet(i.v)
            elif isinstance(i, SET):
                self.visitSet(i)

    def visitAttribute(self, attribute:SET, last):
        self.visitSet(attribute)


class independentAttributesRemover(astTransformer):
    def visitEventRule(self, rule):
        for istate in rule.lhs:
            for i in istate.attributes.v:
                if isinstance(i, PAIR):
                    #print(i.k, type(i.v.v[0]))
                    if isinstance(i.v, SET):
                        if isinstance(i.v.v[0], DOTS):#since pair value are always SET
                            istate.attributes.remove(i)
                    else:
                        if isinstance(i.v, DOTS):
                            istate.attributes.remove(i)
            if not istate.attributes.has(DOTS()):
                istate.attributes.add(DOTS())#supplement

class varTypesAdder(astTransformer):
    def __init__(self, varTypes:dict[str,str]):
        super().__init__()
        self.varTypes = varTypes
    def addVar(self, rule):
        T = astTransformer
        def anotateTypes(v):
            if v.ident in self.varTypes:
                v.type_ = self.varTypes[v.ident]
            return v
        rule.visit([(T.matchVar, anotateTypes)])
    def visitStateRule(self,rule):
        return self.addVar(rule)
    def visitEventRule(self,rule):
        return self.addVar(rule)
    def visitProposition(self, prop):
        return self.addVar(prop.constraint)

class repeatedInternalStatesMerger(astTransformer):
    def visitStateRule(self, rule):
        for is_or_e in rule.lhs:
            pass
        #TODO

class missingInStateAdder(astTransformer):
    def visitStateRule(self, rule):
        '''
        check if any missing Internal State on any side of equational rules
        '''
        lhsPrinInStates = {}
        rhsPrinInStates = {}

        for is_or_e in rule.lhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                lhsPrinInStates[istate.principal] = istate
        for is_or_e in rule.rhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                rhsPrinInStates[istate.principal] = istate

        if lAddSet := set(lhsPrinInStates.keys()) - set(rhsPrinInStates.keys()):
            for prin in lAddSet:
                rule.rhs.append(lhsPrinInStates[prin]) 
        if rAddSet := set(rhsPrinInStates.keys()) - set(lhsPrinInStates.keys()):
            for prin in rAddSet:
                rule.lhs.append(rhsPrinInStates[prin]) 
        return rule

class missingVariableInstate(astTransformer):
    def visitEventRule(self, rule):
        T = astTransformer
        lhsPrins = []#variable principals in lhs
        def collectVarPin(v):
            nonlocal lhsPrins
            if v.type_ in PrinTypes:
                lhsPrins.append(v)
            return v
        for istate in rule.lhs:
            istate.visit([(T.matchVar,collectVarPin)])
        for param in rule.rhs.params:
            if isinstance(param, VARIABLE):
                if param.type_ in PrinTypes and param not in lhsPrins:
                    lhsPrins.append(param)
                    rule.lhs.append(INTERNAL_STATE(param, DOTS()))
        return rule

class missingAttributesAdderBak(astTransformer):
    def visitStateRule(self, rule):
        '''
        check if any missing attributes on any side of equational rules
        '''
        lhsPrinAttributes = {}#principal:attributes
        rhsPrinAttributes = {}

        for is_or_e in rule.lhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                lhsPrinAttributes[istate.principal] = istate.attributes
        for is_or_e in rule.rhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                rhsPrinAttributes[istate.principal] = istate.attributes
        for commonPrin in set(lhsPrinAttributes.keys()).intersection(set(rhsPrinAttributes.keys())):
            if lAddSet := set(lhsPrinAttributes[commonPrin].keys()) - set(rhsPrinAttributes[commonPrin].keys()):
                for attKey in lAddSet:
                    rhsPrinAttributes[commonPrin].add(deepcopy(lhsPrinAttributes[commonPrin].get(attKey)))
            if rAddSet := set(rhsPrinAttributes[commonPrin].keys()) - set(lhsPrinAttributes[commonPrin].keys()):
                for attKey in rAddSet:
                    lhsPrinAttributes[commonPrin].add(deepcopy(rhsPrinAttributes[commonPrin].get(attKey)))
                    
        return rule

class missingAttributesAdder(astTransformer):
    #TODO recursively convert attributes in deeper set
    def visitStateRule(self, rule):
        '''
        check if any missing attributes on any side of equational rules
        '''
        lhsPrinAttributes = {}#principal:attributes
        rhsPrinAttributes = {}

        for is_or_e in rule.lhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                lhsPrinAttributes[istate.principal] = istate.attributes
        for is_or_e in rule.rhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                rhsPrinAttributes[istate.principal] = istate.attributes
        for commonPrin in set(lhsPrinAttributes.keys()).intersection(set(rhsPrinAttributes.keys())):
            if lAddSet := set(lhsPrinAttributes[commonPrin].keys()) - set(rhsPrinAttributes[commonPrin].keys()):
                for attKey in lAddSet:
                    rhsPrinAttributes[commonPrin].add(deepcopy(lhsPrinAttributes[commonPrin].get(attKey)))
            if rAddSet := set(rhsPrinAttributes[commonPrin].keys()) - set(lhsPrinAttributes[commonPrin].keys()):
                for attKey in rAddSet:
                    lhsPrinAttributes[commonPrin].add(deepcopy(rhsPrinAttributes[commonPrin].get(attKey)))
                    
        return rule

class freshTransformer(astTransformer):
    def visitStateRule(self, rule):
        '''
        check if some Fresh is rhs.
        If so, convert them with built-in function randomStr(...,N),
        and convert rhs counter to N+1
        '''
        l = []
        T = astTransformer
        def collectFresh(v:VARIABLE):
            nonlocal l
            if v.ident.startswith('Fresh'):
                l.append(v)
            return v
        for is_or_e in rule.rhs:
            is_or_e.visit([(T.matchVar,collectFresh)])
        rhsFreshList = set(l)
        for fr in rhsFreshList:
            for is_or_e in rule.rhs:
                is_or_e.visit([(lambda x:x==fr, T.randomStr)])
        if len(rhsFreshList)>0:
            for is_or_e in rule.rhs:
                if isinstance(is_or_e, INTERNAL_STATE):
                    istate = is_or_e
                    if istate.principal.ident == 'system':
                        if att := istate.attributes:
                            if pair := att.get(QID("'counter'")):
                                pair.v = ARITH(VARIABLE('N','Nat'),'+','1')
        #remove all the Fresh pairs in premise
        #toRemove = []
        #def collectFreshPair(p:PAIR):
        #    nonlocal toRemove
        #    if isinstnace(p.v,VARIABLE):
        #        if p.v.ident.startswith('Fresh'):
        #            toRemove.append(p)
        #        return p
        #print(toRemove)
        #for is_or_e in rule.lhs:
        #    is_or_e.visit([(lambda x:isinstnace(x,PAIR), collectFreshPair)])
        #for is_or_e in rule.lhs:
        #    if isinstnace(is_or_e, INTERNAL_STATE):
        #        istate = is_or_e
        #        for i in toRemove:
        #            istate.attributes.remove(i)
        #


class freshTransformerBak(astTransformer):
    def visitStateRule(self, rule):
        '''
        check if some Fresh is first appeared in rhs, but not in the lhs.
        If so, convert them with built-in function randomStr(...,N)
        '''
        l = []
        T = astTransformer
        def collectFresh(v):
            nonlocal l
            if v.ident.startswith('Fresh'):
                l.append(v)
            return v
        for is_or_e in rule.lhs:
            is_or_e.visit([(T.matchVar,collectFresh)])
        lhsFreshList = set(l)
        l = []
        for is_or_e in rule.rhs:
            is_or_e.visit([(T.matchVar,collectFresh)])
        rhsFreshList = set(l)
        for fr in rhsFreshList - lhsFreshList:
            for is_or_e in rule.rhs:
                is_or_e.visit([(lambda x:x==fr, T.randomStr)])
        for is_or_e in rule.rhs:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                if istate.principal.ident == 'system':
                    if att := istate.attributes:
                        if pair := att.get(QID("'counter'")):
                            pair.v = ARITH(VARIABLE('N','Nat'),'+','1')

class systemStateAdder(astTransformer):
    def __init__(self,hasFresh=False,hasCurrentTime=False):
        super().__init__()
        self.hasFresh = hasFresh#across the whole ast
        self.hasCurrentTime = hasCurrentTime

    def visitStateRule(self, rule):
        T = astTransformer
        testBool = False
        def test(x):
            nonlocal testBool
            testBool = True
            return x
        for is_or_e in rule.lhs:
            is_or_e.visit([(allf(T.matchVar,T.matchFresh),test)])
        for is_or_e in rule.rhs:
            is_or_e.visit([(allf(T.matchVar,T.matchFresh),test)])
        hasFresh = testBool
        testBool = False
        if hasFresh: self.hasFresh = True

        for is_or_e in rule.lhs:
            is_or_e.visit([(allf(T.matchVar,T.matchCTime),test)])
        for is_or_e in rule.rhs:
            is_or_e.visit([(allf(T.matchVar,T.matchCTime),test)])
        if rule.condition:
            rule.condition.visit([(allf(T.matchVar,T.matchCTime),test)])
        hasCurrentTime = testBool#for single state rule
        if hasCurrentTime: self.hasCurrentTime = True

        if hasFresh or hasCurrentTime:
            principal = PRINCIPAL('Principal','system')
            attributes = SET()
            if self.hasCurrentTime:
                attributes.add(PAIR(QID("'time'"),VARIABLE('CurrentTime', 'Nat')))
            if self.hasFresh:
                attributes.add(PAIR(QID("'counter'"),VARIABLE('N', 'Nat')))
            attributes.add(DOTS())
            systemState = INTERNAL_STATE(principal, attributes)
            #print(systemState)
            rule.lhs.insert(0, systemState)
            rule.rhs.insert(0, deepcopy(systemState))

    def visitInit(self,rule):
        principal = PRINCIPAL('Principal','system')
        attributes = SET()
        if self.hasFresh or self.hasCurrentTime:
            principal = PRINCIPAL('Principal','system')
            attributes = SET()
            if self.hasCurrentTime:
                attributes.add(PAIR(QID("'time'"), 0))
            if self.hasFresh:
                attributes.add(PAIR(QID("'counter'"),0))
            attributes.add(DOTS())
            systemState = INTERNAL_STATE(principal, attributes)
            rule.istates.insert(0, systemState)

    def addEachSystemTime(self, rule:EVENT_RULE):
        #add each event rule system time if hasCurrentTime
        if self.hasCurrentTime:
            principal = PRINCIPAL('Principal','system')
            attributes = SET()
            if self.hasCurrentTime:
                attributes.add(PAIR(QID("'time'"), VARIABLE('N','Nat')))
            attributes.add(DOTS())
            systemState = INTERNAL_STATE(principal, attributes)
            rule.lhs.insert(0, systemState)

def transformStateRule(ast:AST):
    ssa = systemStateAdder()
    ssa.visit(ast)
    freshTransformer().visit(ast)
    missingInStateAdder().visit(ast)
    missingAttributesAdder().visit(ast)
    dotsDisduper().visit(ast)
    dotsAdder().visit(ast)
    dotsFixer().visit(ast)
    return ssa.hasFresh, ssa.hasCurrentTime

def transformEventRule(ast:AST, hasCurrentTime = False):
    independentAttributesRemover().visit(ast)
    missingVariableInstate().visit(ast)
    #ssa = systemStateAdder(False, hasCurrentTime)#add each event rule system time if hasCurrentTime
    #ssa.visit(ast)
    dotsDisduper().visit(ast)
    dotsAdder().visit(ast)
    dotsFixer().visit(ast)
    return ast

def transformProposition(ast:AST):
    dotsDisduper().visit(ast)
    dotsAdder2().visit(ast)
    dotsFixer().visit(ast)
    return ast

def transformInit(ast:AST, hasFresh=False, hasCurrentTime=False):
    ssa = systemStateAdder(hasFresh, hasCurrentTime)
    ssa.visit(ast)
    dotsRemover().visit(ast)
    return ast

def addVarTypes(ast:AST, varTypes:dict[str,str]):
    varTypesAdder(varTypes).visit(ast)
    return ast

def defaultVariables():
    {'N':'Nat'}

if __name__ == '__main__':
    def test1():
        code4 = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceX | ... > $ UserX 'pressButton' DeviceX
=> < DeviceX | ... > $ DeviceX 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceX : ('tickets': SetX , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceX : ('tickets': (SetX, ('key': KeyA, 'time': CurrentTime)) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceX 
=> < cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ cloudA 'send' UserX | KeyA if CurrentTime < TimeA + 1 .

< cloudA | DeviceX : ('owner': nils , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserX) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > .

< cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ cloudA 'send' UserX | 'userUid': UserY .

< cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:join' cloudA | ('userUid': UserY ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserY, UserX) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > 
=> < cloudA | DeviceX : ('tickets': (...) , ...) > if CurrentTime > TimeA + 2 .

< UserX | 'knowledge': SetX , ... > $ cloudA 'send' UserX | KeyA
=> < UserX | 'knowledge': (SetX, KeyA) , ... > .

< UserX | 'knowledge': SetX , ... > $ cloudA 'send' UserX | 'userUid': UserY
=> < UserX | 'knowledge': (SetX, 'userUid': UserY) , ... > .
'''
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | 'secret' : nils , 'freshSecret' : FreshSecret , ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | 'secret' : FreshSecret , 'freshSecret' : FreshSecret , ... > $ DeviceY 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceY : ('tickets' : SetX , 'currentTime' : CurrentTime , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetX, ('key' : KeyA, 'time' : CurrentTime)) , 'currentTime' : CurrentTime , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ cloudA 'sendKey' UserX | KeyA if CurrentTime < TimeA + 1 .

< cloudA | DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > .

< cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > $ cloudA 'sendUID' UserX | 'userYid' .

< cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > $ UserX 'callAPI:join' cloudA | ('userYid' ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY, UserX) , 'tickets' : (('key' : KeyA, ...) , ...) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , 'currentTime' : CurrentTime , ...) >
=> < cloudA | DeviceY : ('tickets' : nils , 'currentTime' : CurrentTime , ...) > if CurrentTime > TimeA + 2 .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendKey' UserX | KeyA
=> < UserX | 'knowledge' : (SetX, KeyA) , ... > .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendUID' UserX | UID
=> < UserX | 'knowledge' : (SetX, UID) , ... > .
        '''
        code2 = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | ... > $ DeviceY 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceY : ('tickets' : SetX , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetX, ('key' : KeyA, 'time' : CurrentTime)) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ cloudA 'sendKey' UserX | KeyA
if CurrentTime < TimeA + 1 .

< cloudA | DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > .

< cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ cloudA 'sendUID' UserX | 'userYid' .

< cloudA | DeviceY : ('owner' : (UserY) , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > $ UserX 'callAPI:join' cloudA | ('userYid' ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY, UserX) , 'tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA) , ...) , ...) >
=> < cloudA | DeviceY : ('tickets' : nils , ...) >
if CurrentTime > TimeA + 2 .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendKey' UserX | KeyA
=> < UserX | 'knowledge' : (SetX, KeyA) , ... > .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendUID' UserX | UID
=> < UserX | 'knowledge' : (SetX, UID) , ... > .
        '''
        code4 = '''\
< deviceLock | 'trustSet': (PrincipalX, ...), 'state': false, ... > $ PrincipalX 'callAPI:toggle' deviceLock
=> < deviceLock | 'trustSet': (PrincipalX, ...), 'state': true, ... > .

< CloudX | DeviceY : ('trustSet': (PrincipalX, ...), 'state': false, ...), ... > $ PrincipalX 'callAPI:toggle' DeviceY
=> < CloudX | DeviceY : ('trustSet': (PrincipalX, ...), 'state': true, ...), ... > $ CloudX 'callAPI:toggle' DeviceY .

< cloudSmartThing | DeviceX : ('boundTo': DeviceY, ...), ... > $ cloudSmartThing 'action' DeviceX
=> < cloudSmartThing | DeviceX : ('boundTo': DeviceY, ...), ... > $ cloudSmartThing 'action' DeviceY .

< CloudX | DeviceY : ('trustSet': (UserX, ...), 'key': KeyA, ...), ... > $ UserX 'callAPI:getKey' CloudX
=> < CloudX | DeviceY : ('trustSet': (UserX, ...), 'key': KeyA, ...), ... > $ CloudX 'sendKey' UserX | KeyA .

< UserX | 'key': nils, ... > $ CloudX 'sendKey' UserX | KeyA
=> < UserX | 'key': KeyA, ... > .

< CloudX | DeviceY : ('trustSet': (UserX, ...), ...), ... > $ UserX 'callAPI:delegate' CloudX | (UserZ; DeviceY)
=> < CloudX | DeviceY : ('trustSet': (UserX, UserZ, ...), ...), ... > .

< CloudX | DeviceY : ('trustSet': (UserX, UserZ, ...), ...), ... > $ UserX 'callAPI:revoke' CloudX | (UserZ; DeviceY)
=> < CloudX | DeviceY : ('trustSet': (UserX, ...), ...), ... > .

< cloudSmartThing | DeviceY : ('key': KeyA, ...), ... > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceY; KeyA)
=> < cloudSmartThing | DeviceY : ('trustSet': (PrincipalX, ...), 'key': KeyA, ...), ... > .
        '''
        ast = parseAST(code4)
        vtypes = {
          "CurrentTime": "Nat",
          "KeyA": "Qid",
          "FreshSecret": "Qid",
          "SetX": "Set",
          "TimeA": "Nat",
          "UserY": "User",
          "UserX": "User",
          "DeviceY": "Device",
          "UID": "Qid"
        }
        vtypes4 = {
          "UserX": "User",
          "PrincipalX": "Principal",
          "DeviceY": "Device",
          "CloudX": "Cloud",
          "DeviceX": "Device",
          "KeyA": "Qid",
          "UserZ": "User"
        }
        addVarTypes(ast, vtypes4)
        transformStateRule(ast)
        print(ast)
    def test2():
        code = '''\
< UserX | 'localTo' : true , ... > < DeviceY | ... > => ev3(UserX, DeviceY) .
< UserX | 'localTo' : true , ... > < DeviceY | ... > => ev7(UserX, DeviceY) .
< UserX | 'localTo' : true , 'key' : KeyA , ... > < DeviceY | ... > => ev4(UserX, DeviceY, KeyA) .
< UserX | 'localTo' : ... , 'key' : KeyA , ... > < DeviceY | ... > => ev6(UserX, DeviceY, KeyA) .
< UserX | 'localTo' : ... , 'key' : KeyA , ... > => ev9(UserX, DeviceY, KeyA) .
< UserX | 'localTo' : true , ... > < DeviceY | ... > => ev2(UserX, DeviceY) .
< UserX | 'localTo' : false , ... > < DeviceY | ... > => ev1(UserX, DeviceY) .
        '''
        code2 = '''\
< UserX | 'localTo' : DeviceY > => ev1(UserX, DeviceY) .
< UserX | 'hasKey' : KeyA > => ev2(UserX, DeviceY, KeyA) .
< UserX | 'hasKey' : KeyA > => ev3(UserX, DeviceY) .
< UserX | 'localTo' : DeviceY > => ev4(UserX, DeviceY) .
< UserX | 'localTo' : nils > => ev5(UserX, DeviceY) .
        '''
        ast = parseAST(code2)
        addVarTypes(ast,{'DeviceY':'Device','UserX':'User','KeyA':'Qid'})
        transformEventRule(ast,True)
        print(ast)
    def test3():
        code = '''\
< cloudA | DeviceY : ('bdKey' : KeyA , 'owner' : nils , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
< DeviceY | 'isOnline': true , 'owner': nils , ... >
=> < cloudA | DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ...) > < DeviceY | 'owner': UserX , ... > .\
        '''
        code = '''\
< cloudA | UserX : ('key' : KeyA , ...) , DeviceY : ('owner' : nils , ...) > $ DeviceY 'callAPI:bind' cloudA | KeyA
=> < cloudA | UserX : ('key' : KeyA , ...) , DeviceY : ('owner' : UserX , ...) > .
        '''
        ast = parseAST(code)
        dotsAdder().visit(ast)
        dotsFixer().visit(ast)
        print(ast)
    def test4():
        code = '''\
ap1 =| $ userA Act PrincipalA .
ap2 =| $ DeviceY 'callAPI:setKey' cloudA | (FreshSecret) .
ap3 =| < cloudA | deviceB : (... , 'owner' : userA , ...) > .
ap4 =| $ userC Act PrincipalA .
ap5 =| $ UserX Act PrincipalA .
ap6 =| < userC | 'localTo' : deviceB , ... > .
ap7 =| < cloudA | deviceB : (... , 'owner' : userC , ...) > .
        '''
        code2 = '''\
ap1 =| $ userA 'callAPI:delegate' cloudGoogle | (UserZ ; DeviceY) .
ap2 =| $ userA 'callAPI:revoke' cloudGoogle | (UserZ ; DeviceY) .
ap3 =| $ userA Act PrincipalX .
ap4 =| $ userC Act PrincipalX .
ap5 =| < deviceLock | 'state' : false , ... > .
ap6 =| < deviceSwitch | 'trust' : (userC) , ... > .
ap7 =| < deviceLock | 'state' : true , ... > .
        '''
        ast = parseAST(code2)
        transformProposition(ast)
        print(ast)
    def test5():
        code = '''\
< userA | ('knowledge' : nils , 'localTo' : deviceB) > < userC | ('knowledge' : nils , 'localTo' : nils) > < deviceB | nils > < cloudA | deviceB : ('tickets' : nils , 'owner' : nils) >
        '''
        ast = parseInitAST(code)
        print(type(ast))
        transformInit(ast,True,True)
        print(ast)
    test4()

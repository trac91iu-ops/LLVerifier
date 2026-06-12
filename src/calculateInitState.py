#!/bin/python3
from lark import Lark, Transformer ,Tree, Token, Visitor
import copy
import pdb
from AST import *


IStateMAP:dict[str,SET] = {}#key:prinname,value:attributes

def addDefaultAttributes():
    #DEPORECATED
    for k,v in IStateMAP.items():
        if k in ['userA','userC']:
            #modify v
            v.add(PAIR(QID('know'),SET(QID('secret'+k[-1]))))

def removeUselessFromAttributes():
    def helper(s):
        if isinstance(s,DOTS):
            s = SET()
        elif isinstance(s,SET):
            s.remove(DOTS())
            s.remove(NILS())
            helper(s.v)
        elif isinstance(s,PAIR):
            helper(s.v)
        elif isinstance(s,tuple):
            for i in s:
                helper(i)
    for k,v in IStateMAP.items():
        helper(v)

def typeAnnotate4IstateMAP():
    #DEPORECATED
    def changeVal(ptr,v,idx=0):
        if isinstance(ptr,str):
            IStateMAP[ptr] = v2type(v)
        elif isinstance(ptr,SET):
            ptr.update(idx,v2type(v))
        else:
            print('wrong!')
    for k,v in IStateMAP.items():
        modifyLeaves(k,v,0,changeVal)

def genInitTemplate():
    #typeAnnotate4IstateMAP()
    removeUselessFromAttributes()
    #addDefaultAttributes()
    l = []
    for k,v in IStateMAP.items():
        l.append(INTERNAL_STATE(k,v))
    return ' '.join([str(istate) for istate in l])


def populateIStateMap(varmap,tree): 
    attributesCombiner(varmap).visit(tree)
    for k,v in IStateMAP.items():
        attributesCombinerPostprocess(v)

annotateTypes = lambda tree: typesAnnotator().visit(tree)

def v2type(s):
    downcase = lambda i : i[0]+i[1:].lower()
    if isinstance(s,VARIABLE):
        if not s.type_:
            print('Error: has not set the type for variable:', VARIABLE.ident)
            exit(1)
        return TYPE(s.type_)
    elif isinstance(s,QID) or isinstance(s,int):
        return s
    else:
        return TYPE(downcase(s.__class__.__name__))

def modifyLeaves(ptr,s,i,f):
    '''
    Modify leaf element using pointer ptr and callback function f, replacing s, record index in i
    '''
    if isinstance(s,INTERNAL_STATE):
        modifyLeaves(s,s.attributes,i,f)
    elif isinstance(s,SET):
        modifyLeaves(s,s.v,i,f)
    elif isinstance(s,PAIR):
        modifyLeaves(s,s.k,i,f)
        modifyLeaves(s,s.v,i,f)
    elif isinstance(s,tuple) or isinstance(s,set):
        for idx,item in enumerate(s):
            modifyLeaves(ptr,item,idx,f)
    elif isinstance(s,DOTS) or isinstance(s,NILS):
        return
    elif isinstance(s,VARIABLE):
        f(ptr,s,i)
    else: #QID,BOOL,etc
        f(ptr,s,i)

class typesAnnotator(ASTVisitor):
    def visitInState(self,i,last):
        def changeVal(ptr,v,idx=0):
            if isinstance(ptr,str):
                IStateMAP[ptr] = v2type(v)
            elif isinstance(ptr,SET):
                ptr.update(idx,v2type(v))
            elif isinstance(ptr,PAIR):
                if v == ptr.k:
                    ptr.k = v2type(v)
                elif v == ptr.v:
                    ptr.v = v2type(v)
                else:
                    print('wrong',ptr)
            elif isinstance(ptr,typesAnnotator):
                pass
            else:
                print('wrong!',ptr)

        modifyLeaves(last,i,0,changeVal) 

def combineAttributes(a1:SET, a2:SET):
    a1 = SET.disduplicate(a1)
    a2 = SET.disduplicate(a2)
    a3 = copy.deepcopy(a2)
    result = a3
    if isinstance(a1, SET) and isinstance(a1, SET):
        #disduplicate
        for att in a1.v:
            if isinstance(att, PAIR):
                if att.k in a3.keys():
                    att3 = a3.get(att.k)
                    a3v = a3.vals(att.k)
                    #att3.v = combineAttributes(att3.v,att.v)
                    if not isinstance(att.v,SET):
                        sl = SET(att.v)#change back after 
                    else:
                        sl = att.v
                    if not isinstance(att3.v,SET):
                        sr = SET(att3.v)
                    else:
                        sr = att3.v
                    att3.v = combineAttributes(sl,sr)
                else:
                    if att not in a3.v:
                        #print('in1',att,a3.v)
                        a3.add(att)
            elif isinstance(att,DOTS) or isinstance(att,NILS):
                #print('in1')
                pass
            else:#item
                if isinstance(att, SET):
                    att = att.removeByType(DOTS)
                if att not in a3.v:
                    notAdd = False
                    #print('in2',att,a3.v)
                    if isinstance(att,SET):
                        for a3s in a3.v:
                            if isinstance(a3s,SET):
                                if SET.containOrContained(att,a3s):
                                    notAdd = True
                    if not notAdd:
                        a3.add(att)
                        result = CHOICES.makeFromSet(a3)
    return result


class attributesCombiner(ASTVisitor):
    def __init__(self,varmap):
        self.varmap = varmap
        super().__init__()
    def visitInState(self,i,last):
        principal = i.principal
        attributes = i.attributes
        if isinstance(principal,VARIABLE):
            #lookup type
            if self.varmap[principal.ident] == 'User':
                prinnames = ['userA','userC']#ADHOC!
            else: #self.varmap[principal.ident] in ['Device','Server','App','Cloud']:
                downcase = lambda a : a[0].lower()+a[1:]
                #downcase = lambda a : a.lower()
                prinnames = [downcase(self.varmap[principal.ident])+'B']
        else:
            prinnames = [principal.ident]
        for prinname in prinnames:
            #print('handle',i,prinname)
            if prinname in IStateMAP:
                IStateMAP[prinname] = combineAttributes(IStateMAP[prinname],attributes)
            else:
                IStateMAP[prinname] = attributes

def attributesCombinerPostprocess(attributes:SET):
    matchSet = lambda x:type(x) == SET
    def helper(s:SET):
        if len(s.v) == 1:
            return s.v[0]
        else:
            return s
    attributes.visit([(matchSet, helper)])
    return attributes

def removeItemInSetItem(ast:AST):
    def helper(s:SET):
        typeset = lambda x:isinstance(x, TYPE) and x.v == 'Set'
        if len(s.v) == 2:
            if typeset(s.v[0]):
                s.remove(s.v[1])
            elif typeset(s.v[1]):
                s.remove(s.v[0])
        return s
    for k,attributes in IStateMAP.items():
        attributes.visit([(lambda x:isinstance(x,SET), helper)])
    return ast

def calculateInitState(ast:AST,varmap:dict[str,str]):
    ast = copy.deepcopy(ast)
    annotateTypes(ast)
    populateIStateMap(varmap,ast)
    removeItemInSetItem(ast)
    return genInitTemplate()

def calculateInitStateFromCode(code:str,varmap:dict[str,str]):
    ast = parseAST(code,varmap)
    return calculateInitState(ast,varmap)

def test(code,varmap):
    from analyze import extractVarsFromAST
    ast = parseAST(code,varmap)
    variables = extractVarsFromAST(ast)
    print(ast)
    print()
    print(variables)

    annotateTypes(ast)
    print(ast)
    print()

    populateIStateMap(varmap,ast)
    print(IStateMAP)
    removeItemInSetItem(ast)
    print(genInitTemplate())
    #print(IStateMAP)

    return ast   
if __name__ == '__main__':
    # Example of parsing an Les rule
    code = '''\
< UserX | 'knowledge' : SetK , ... > $ cloudA 'send' UserX | KeyA
=> < UserX | 'knowledge' : (SetK , KeyA) , ... > .

< UserX | 'knowledge' : SetK , ... > $ cloudA 'send' UserX | UserY
=> < UserX | 'knowledge' : (SetK , UserY) , ... >   .
    '''
    code3 = '''\
< cloudA | DeviceY : ('tickets' : (SetT , ('key': KeyA , 'time' : CurrentTime , ...)) , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetT , ('key' : KeyA , 'time' : CurrentTime)) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA), SetT) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , SetT) , ...) > $ cloudA 'send' UserX | KeyA if CurrentTime < TimeA + 1 .
    '''
    code2 = '''\
< DeviceY | 'freshSecret' : FreshSecret , ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | 'freshSecret' : FreshSecret , ... > $ DeviceY 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceY : ('tickets' : (SetT , ('time' : CurrentTime , ...)) , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetT , ('key' : KeyA , 'time' : CurrentTime)) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA), SetT) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , SetT) , ...) > $ cloudA 'send' UserX | KeyA if CurrentTime < TimeA + 1 .

< cloudA | DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , ...), SetT) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : UserX , 'tickets' : (('key' : KeyA , ...) , SetT) , ...) > .

< cloudA | DeviceY : ('owner' : UserY , 'tickets' : (('key' : KeyA , ...), SetT) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : UserY , 'tickets' : (('key' : KeyA , ...), SetT) , ...) > $ cloudA 'send' UserX | UserY .

< cloudA | DeviceY : ('owner' : UserY , 'tickets' : (('key' : KeyA , ...), SetT) , ...) > $ UserX 'callAPI:join' cloudA | (UserY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY , UserX) , 'tickets' : (('key' : KeyA , ...), SetT) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA), SetT) , ...) >
=> < cloudA | DeviceY : ('tickets' : SetT , ...) > if CurrentTime > TimeA + 2 .

< UserX | 'knowledge' : SetK , ... > $ cloudA 'send' UserX | KeyA
=> < UserX | 'knowledge' : (SetK , KeyA) , ... > .

< UserX | 'knowledge' : SetK , ... > $ cloudA 'send' UserX | UserY
=> < UserX | 'knowledge' : (SetK , UserY) , ... > .
'''
    code4 = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceX | ... > $ UserX 'pressButton' DeviceX
=> < DeviceX | ... > $ DeviceX 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceX : ('tickets': SetT , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceX : ('tickets': (SetT, ('key': KeyA, 'time': CurrentTime)) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceX 
=> < cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ cloudA 'send' UserX | KeyA if CurrentTime < TimeA + 1 .

< cloudA | DeviceX : ('owner': nils , 'tickets': (('key': KeyA, ...) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserX) , 'tickets': (('key': KeyA, ...) , ...) , ...) > .

< cloudA | DeviceX : ('owner': (UserY , ...) , 'tickets': (('key': KeyA, ...) , ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserY , ...) , 'tickets': (('key': KeyA, ...) , ...) , ...) > $ cloudA 'send' UserX | 'UID': UserY .

< cloudA | DeviceX : ('owner': (UserY , ...) , 'tickets': (('key': KeyA, ...) , ...) , ...) > $ UserX 'callAPI:join' cloudA | ('UID': UserY ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserY , UserX , ...) , 'tickets': (('key': KeyA, ...) , ...) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > 
=> < cloudA | DeviceX : ('tickets': (...) , ...) > if CurrentTime > TimeA + 2 .

< UserX | 'knowledge': SetK , ... > $ cloudA 'send' UserX | KeyA
=> < UserX | 'knowledge': (SetK, KeyA) , ... > .

< UserX | 'knowledge': SetK , ... > $ cloudA 'send' UserX | 'UID': UserY
=> < UserX | 'knowledge': (SetK, 'UID': UserY) , ... > .
    '''
    code5 = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | ... > $ DeviceY 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceY : ('tickets' : SetX , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetX, ('key' : KeyA, 'time' : CurrentTime)) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ cloudA 'send' UserX | KeyA if CurrentTime < TimeA + 1 .

< cloudA | DeviceY : ('owner' : nils, 'tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserX), 'tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > .

< cloudA | DeviceY : ('owner' : SetX, 'tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (SetX, UserX), 'tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...) , ...) >
=> < cloudA | DeviceY : ('tickets' : nils , ...) > if CurrentTime > TimeA + 2 .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'send' UserX | KeyA
=> < UserX | 'knowledge' : (SetX, KeyA) , ... > .
    '''
    varmap4 = {'UserX': 'User', 'DeviceY': 'Device', 'DeviceX':'Device','SetT':'Set', 'SetK':'Set', 'KeyA': 'Qid', 'KeyB': 'Qid', 'CurrentTime' : 'Int', 'TimeA': 'Int', 'UserY':'User', 'FreshSecret' : 'Qid'}
    varmap5 = {
      "DeviceY": "Device",
      "FreshSecret": "Qid",
      "KeyA": "Qid",
      "SetX": "Set",
      "UserX": "User",
      "CurrentTime": "Nat",
      "TimeA": "Nat"
    }
    #a = test(code4, varmap4)
    a = test(code5, varmap5)
    #print(str(a))

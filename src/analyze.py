#!/bin/python3
from AST import *
from copy import deepcopy

def extractVarsFromAST(ast:AST)->list[VARIABLE]:
    def matchVar(x): return type(x) == VARIABLE
    s = set()
    def helper(v:VARIABLE):
        nonlocal s
        s.add(v)
        return v
    ast.visit([(matchVar, helper)])
    return list(s)

def extractVarsFromCode(code:str)->list[VARIABLE]:
    ast = parseAST(code)
    return extractVarsFromAST(ast)

def toVarTypeDecls(vtypes:dict)->str:
    return '\n'.join([f"vars {v} : {t} ." for v,t in vtypes.items()])

def extractEventsFromAST(ast:AST)->list[EVENT]:
    def matchEvent(x): return type(x) == EVENT
    l = []#keep order
    def helper(v:EVENT):
        nonlocal l
        if v not in l:
            l.append(v)
        return v
    ast.visit([(matchEvent, helper)])
    return l

def extractEventsFromCode(code:str)->list[EVENT]:
    AST = parseAST(code)
    return extractEventsFromAST(AST)

def giveEvtDecls(es:list[EVENT])->list[EVENT_DECL]:
    '''
    convert event list `es` to a a list of event declaration objects.
    Each declaration contains a event reference with index and parameter list.
    If an event has compound argument, generate two declarations for different modeling need of event rules.
    '''
    idx = 1
    l = []
    def helper(args:LIST):
        nonlocal compound, params_lst2
        for arg in args.v:
            if isinstance(arg,VARIABLE):
                params_lst2.append(arg)
            elif isinstance(arg, LIST):
                helper(arg)
            elif isinstance(arg, FUNCALL):
                compound = True
                for param in arg.params:
                    if isinstance(param, VARIABLE):
                        params_lst2.append(param)
            else:
                print('[-] Warning in function giveEvtDecls, unhandled argument type:',type(arg))
    #def addIfNot(edecl:EVENT_DECL, l:LIST):
    #    if edecl.event not in [e.event for e in l]:
    #        l.append(edecl)

    for e in es:
        params_lst1:list[VARIABLE] = []
        params_lst2:list[VARIABLE] = []
        compound  = False
        if isinstance(e.subject,VARIABLE):
            params_lst1.append(e.subject)
        if isinstance(e.object,VARIABLE):
            params_lst1.append(e.object)
        if e.arguments:
            helper(e.arguments)

        l.append(EVENT_DECL(f'ev{idx}',e,params_lst1 + params_lst2))
        #addIfNot(EVENT_DECL(f'ev{idx}',e,params_lst1 + params_lst2),l)
        idx += 1
        if compound:
            e2 = deepcopy(e) 
            arg_var = VARIABLE('MessageA','Qid') #assume all the funcall returns Qid for now
            e2.arguments = LIST([arg_var])
            l.append(EVENT_DECL(f'ev{idx}',e2,params_lst1 + [arg_var]))
            #addIfNot(EVENT_DECL(f'ev{idx}',e2,params_lst1 + [arg_var]),l)
            idx += 1
    return l


if __name__ == '__main__':
    def test1():
        code1 = '''\
< UserA | 'localTo' : nils , ... > $ UserA 'approach' DeviceB => < UserA | 'localTo' : DeviceB , ... > .
< UserA | 'localTo' : DeviceB , ... > $ UserA 'leave' DeviceB => < UserA | 'localTo' : nils , ... > .
< DeviceB | 'pressed' : false , ... > $ UserA 'press' DeviceB => < DeviceB | 'pressed' : true , ... > .
< DeviceX | 'pressed' : true , 'key' : nils , ... > $ UserA 'callAPI:setKey' DeviceX | (NewKey) => < DeviceX | 'pressed' : false , 'key' : NewKey , ... > $ DeviceX 'callAPI:setKey' cloudA | (NewKey) .
< DeviceX | 'pressed' : true , 'key' : OldKey , ... > $ UserA 'callAPI:setKey' DeviceX | (NewKey) => < DeviceX | 'pressed' : false , 'key' : NewKey , ... > $ DeviceX 'callAPI:setKey' cloudA | (NewKey) .
< cloudA | DeviceX : ('bdKey' : OldKey , ...) > $ DeviceX 'callAPI:setKey' cloudA | (NewKey) => < cloudA | DeviceX : ('bdKey' : NewKey , ...) > .
< cloudA | DeviceX : ('bdKey' : KeyB , 'owner' : nils , ...) > $ UserA 'callAPI:bind' cloudA | (DeviceX ; KeyB) => < cloudA | DeviceX : ('bdKey' : KeyB , 'owner' : UserA , ...) > if KeyB == KeyB .
< DeviceX | 'pressed' : true , 'key' : SomeKey , ... > $ UserA 'callAPI:getKey' DeviceX => < DeviceX | 'pressed' : false , ... > $ DeviceX 'sendKey' UserA | (SomeKey) .
< UserA | 'key' : OldKey , ... > $ DeviceX 'sendKey' UserA | (NewKey) => < UserA | 'key' : NewKey , ... > .
< cloudA | DeviceX : ('bdKey' : ProvidedKey , 'owner' : OwnerA , ...) > $ UserA 'callAPI:reset' cloudA | (DeviceX ; ProvidedKey) => < cloudA | DeviceX : ('bdKey' : '' , 'owner' : nils , ...) > if ProvidedKey == ProvidedKey .
    '''
        code2 = '''\
< UserA | 'key' : KeyA > < DeviceB | ... > => ev1(UserA, DeviceB, KeyA) .
    '''
        print(extractVarsFromCode(code1))
        vtypes = {'OldKey':'Qid', 'NewKey':'Qid', 'DeviceB':'Device', 'UserA':'User', 'DeviceX':'Device', 'KeyB':'Qid', 'SomeKey':'Qid', 'ProvidedKey':'Qid', 'OwnerA':'User'}
        ast = parseAST(code1, vtypes)
        print(extractEventsFromAST(ast))
        a = {'DeviceB':'Device','UserA':'User','KeyA':'Qid'}
        print(toVarTypeDecls(a))
    def test2():
        code3 ='''\
< deviceB | ('key' : nils , 'pressed' : false) >
< cloudA | userA : ('key' : 'secretA') , userC : ('key' : 'secretC') , deviceB : ('owner' : nils) >
< userA | ('localTo' : deviceB) >
< userC | ('localTo' : nils) >
        '''
        ast = parseInitAST(code3)
        print(ast)
        #print(type(ast.istates[0].attributes.v[0].v))
    def test3():
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | 'key': KeyA , ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | 'key': KeyA , ... > $ DeviceY 'send' UserX | encrypt(KeyA, FreshRandomString) .

< UserX | 'message': nils , ... > $ DeviceY 'send' UserX | MessageA
=> < UserX | 'message': MessageA , ... > .

< cloudA | DeviceY : ('key': KeyA , ...) > $ UserX 'callAPI:bind' cloudA | encrypt(KeyA, FreshRandomString)
=> < cloudA | DeviceY : ('key': KeyA , 'owner': UserX , ...) > .

< cloudA | DeviceY : ('owner': UserX , ...) > $ UserX 'callAPI:reset' cloudA
=> < cloudA | DeviceY : ('owner': nils , ...) > .
        '''
        varmap = {
          "UserX": "User",
          "KeyA": "Qid",
          "FreshRandomString": "Qid",
          "MessageA": "Qid",
          "DeviceY": "Device"
        }
        ast = parseAST(code,varmap)
        elist = extractEventsFromAST(ast)
        print(elist)
        for edecl in giveEvtDecls(elist):
            print(edecl)
    def test4():
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | 'key': KeyA , ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | 'key': FreshKeyA , ... > .

< DeviceY | 'key': KeyA , 'unlocked': true , ... > < UserX | 'key': nils , ... > $ UserX 'callAPI:getKey' DeviceY
=> < DeviceY | 'key': KeyA , 'unlocked': true , ... > < UserX | 'key': KeyA , ... > .

< DeviceY | 'key': KeyA , 'unlocked': true , ... > $ UserX 'callAPI:lock' DeviceY | KeyA
=> < DeviceY | 'key': KeyA , 'unlocked': false , ... > .

< cloudA | UserX : ('devices': nils , 'members': SetX , ...) > $ UserX 'callAPI:invite' UserY
=> < cloudA | UserX : ('devices': nils , 'members': (SetX, UserY) , ...) > .

< cloudA | UserX : ('devices': nils , 'members': (SetX, UserY) , ...) > $ UserX 'callAPI:kick' UserY
=> < cloudA | UserX : ('devices': nils , 'members': SetX , ...) > .

< cloudA | DeviceY : ('owner': UserX , ...) > < cloudA | UserX : ('members': (SetX, UserY) , ...) > < DeviceY | 'key': KeyA , ... > < UserY | 'key': nils , ... > $ UserY 'callAPI:getKey' DeviceY
=> < cloudA | DeviceY : ('owner': UserX , ...) > < cloudA | UserX : ('members': (SetX, UserY) , ...) > < DeviceY | 'key': KeyA , ... > < UserY | 'key': KeyA , ... > .

< DeviceY | 'key': KeyA , ... > < cloudA | DeviceY : ('owner': SetX , ...) > $ UserX 'callAPI:bind' DeviceY | KeyA
=> < DeviceY | 'key': KeyA , ... > < cloudA | DeviceY : ('owner': (SetX, UserX) , ...) > .
        '''
        varmap = {
          "SetX": "Set",
          "FreshKeyA": "Qid",
          "UserY": "User",
          "DeviceY": "Device",
          "UserX": "User",
          "KeyA": "Qid"
        }
        ast = parseAST(code,varmap)
        elist = extractEventsFromAST(ast)
        print(len(elist))
        for edecl in giveEvtDecls(elist):
            print(edecl)
    test4()

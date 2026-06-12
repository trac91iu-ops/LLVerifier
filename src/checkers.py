#!/bin/python3
from collections.abc import Callable
import lark
from DSLSyntax import CheckGrammar as cg
from AST import * 
from analyze import extractVarsFromAST
import re

def pruneErrorMessage(errors)->str:
    delim = 'Expected one of:'
    h,_ = str(errors).split(delim, 1)
    def replace(s:str):
        repls = [('dollar','$'), ('lessthan', '<'), ('equal','=')]
        for original, after in repls:
            s = s.replace(original, after)
        return s

    def exclude(s:str):
        return not 'ANON' in s 
    parser = lark.Lark(cg.dsl_grammar, parser='earley')
    td = {terminal.name:terminal.pattern for terminal in parser.terminals}
    #print(td)
    
    #if 'expected' in errors.__dict__:
    #    el = errors.expected
    if 'allowed' in errors.__dict__:
        el = errors.allowed
    patterns = [str(td[rule]) for rule in filter(exclude,el)]
    #print(patterns)
    #print(errors.char)
    t = delim + ' '+', '.join(set(patterns))
    #t = delim + ' '+', '.join(set([replace(rule.lower()) for rule in filter(exclude,el)]))
    return h+t

def checkComment(s:str)->str|None:
    if '//' in s:
        return 'There should not be any comments in the code block, remove them.'
    else:
        return None

def checkLhsIf(s:str)->str|None:
    try:
        parseAST(s)
    except lark.exceptions.UnexpectedCharacters as e:
        if s[e.pos_in_stream:e.pos_in_stream+2] == 'if':
            allowed = {i for i in e.allowed if not i.startswith('__')}
            if allowed == {'COLON', 'LESSTHAN'}:
                return '`if` clause should not appear in the left hand side of `=>`, put it to the end of state rules just before `.`' 
    return None

def checkAnd(s:str)->str|None:
    if '&&' in s:
        return "use `and` instead of `&&` to express boolean and"
    else:
        return None

def uniqueVars(v:VARIABLE)->bool:
    if v.ident.startswith('Fresh'):
        return True
    if v.ident == 'CurrentTime':
        return True
    return False

def checkRhsNewVariables(code:str)->str|None:
    ast = parseAST(code)
    errors = []
    for rule in ast.rules:
        lhsVars:set[VARIABLE] = set()
        rhsVars:set[VARIABLE] = set()
        for i in rule.lhs:
            lhsVars = lhsVars.union(set(extractVarsFromAST(i)))
        for i in rule.rhs:
            rhsVars = rhsVars.union(set(extractVarsFromAST(i)))
        #remove Fresh
        addVars:str = ','.join([str(i) for i in rhsVars - lhsVars if not uniqueVars(i)])
        #addVars:str = ','.join([str(i) for i in rhsVars - lhsVars])
        if len(addVars) > 0 :
            err= f"Find additional variables {addVars} in right-hand side of state rule {str(rule)}."
            errors.append(err)
    if len(errors)>0:
        comment = 'These variables should appear on the left-hand side (premise) first. To record them, possibly use an attribute in the internal states on the left-hand side.'
        return "[Errors]\n"+'\n'.join(errors)+'\n'+comment
    else:
        return None

def checkTypePlaceHolders(code:str)->str|None:
    l = re.findall(r'\[\w+\]',code)
    if len(l)>0:
        s = set([f'`{i}`'for i in l])
        return f'There should not exist type placeholders. However, I find {','.join(s)}. \nInstantiate them with variables or constants with the same types.'
    return None

def checkAST(s:str)->str|None:
    try:
        parseAST(s)
    except lark.exceptions.UnexpectedCharacters as e:
        return pruneErrorMessage(e)
    except lark.exceptions.UnexpectedEOF as e:
        return pruneErrorMessage(e)
    except Exception as e:
        return str(e)
    return None

def checkINIT(s:str)->str|None:
    try:
        ast = parseInitAST(s)
        vl = extractVarsFromAST(ast)
        if len(vl)>0:
            return f"There should not be variables in init state. However, I found variables {vl}.\nInstantiate them with constants."
    except lark.exceptions.UnexpectedCharacters as e:
        return pruneErrorMessage(e)
    except lark.exceptions.UnexpectedEOF as e:
        return pruneErrorMessage(e)
    except Exception as e:
        return str(e)
    return None

def checkProp(code:str)->str|None:
    try:
        ast = parseAST(code)
    except lark.exceptions.UnexpectedCharacters as e:
        return pruneErrorMessage(e)
    except lark.exceptions.UnexpectedEOF as e:
        return pruneErrorMessage(e)
    except Exception as e:
        return str(e)
    return None

def checkLTL(s:str)->str|None:
    if l := re.findall(r'~\w+',s):
        error_positions = ' and '.join([f"`{i}`" for i in l])
        return f'Detect syntax errors in {error_positions}, but there should be at least one white space after `~` and before the proposition name, add space inside them.'
    else:
        return None

def checkPolicy(policy:str)->str|None:
    return (combine(checkComment, checkAnd, checkLhsIf,checkAST, checkRhsNewVariables))(policy)

def checkTransitions(code:str)->str|None:
    return (combine(checkComment, checkTypePlaceHolders, checkAST))(code)

def combine(*fl:Callable[[str],str|None])->Callable[[str],str|None]:
    def helper(s:str)->str|None:
        for f in fl:
            if e := f(s):
                return e
        return None
    return helper

if __name__ == '__main__':
    def test1():
        #print(checkPolicy("eq < UserA | 'local' : False> = <"))
        prop = '''\
[](O ap7 -> (ap3 /\\ ~ap5))
/\\ <> (~ ap9 /\\ ~ ap10 /\\ O (~ap9 /\\ ap10))
        '''
        print(checkLTL(prop))
    def test2():
        code = '''\
< userA | ('hasKey' : false , ... , 'localTo' : DeviceB) > < userC | ('hasKey' : false , 'localTo' : nils) > < deviceB | ('isOnline' : false , 'owner' : nils , 'key' : Key , 'isPressed' : false) > < cloudA | deviceB : ('bdKey' : 'secret' , 'owner' : nils , ....) >
        '''
        code = '''\
< deviceB | ('secret' : nils , 'owner' : nils) >
< userA | ('local' : true , 'knows' : nils , 'UID' : 'userAid') >
< userC | ('local' : false , 'knows' : nils , 'UID' : 'userCid') >
< cloud | deviceB : ('owner' : nils , 'tickets' : nils) >
        '''
        code = '''\
< deviceLock | ('trustSet' : (cloudSmartThing) , 'state' : false) >
< cloudGoogle | deviceSwitch : ('trustSet' : userA , 'key' : 'secret' , 'state' : false) >
< cloudSmartThing | deviceSwitch : ('key' : 'secret' , 'boundTo' : deviceLock) , cloudGoogle : ('trustSet' : (deviceSwitch)) >
< userA | ('key' : nils) >
< userC | ('key' : nils) >
        '''
        print(checkINIT(code))
    def test3():
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | 'pressed': false , 'online': false , ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | 'pressed': true , 'online': true , ... > $ DeviceY 'sendKey' UserX | KeyA .

< UserX | 'key': nils , ... > $ DeviceY 'sendKey' UserX | KeyA
=> < UserX | 'key': KeyA , ... > .

< cloudA | DeviceY : ('key': KeyA , 'owner': nils , ...) > < DeviceY | 'online': true , 'owner': nils , ... > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('key': KeyA , 'owner': UserX , ...) > < DeviceY | 'online': true , 'owner': UserX , ... > .

< cloudA | DeviceY : ('owner': UserX , ...) > $ UserX 'callAPI:reset' cloudA | DeviceY
=> < cloudA | DeviceY : ('owner': nils , ...) > $ cloudA 'resetDevice' DeviceY .

< DeviceY | 'online': true , 'owner': UserX , ... > $ cloudA 'resetDevice' DeviceY
=> < DeviceY | 'online': false , 'owner': nils , ... > .
        '''
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceX | ... > $ UserX 'pressButton' DeviceX
=> < DeviceX | ... > $ DeviceX 'callAPI:setKey' cloudA | FreshSecret .

< cloudA | DeviceX : ('tickets': SetX , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceX : ('tickets': (SetX, ('key': KeyA, 'time': CurrentTime)) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceX if CurrentTime < TimeA + 1
=> < cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ cloudA 'sendKey' UserX | KeyA .

< cloudA | DeviceX : ('owner': nils , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA)
=> < cloudA | DeviceX : ('owner': (UserX) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > .

< cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceX ; KeyA) if UserY == UID
=> < cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ cloudA 'sendUID' UserX | UID .

< cloudA | DeviceX : ('owner': (UserY) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > $ UserX 'callAPI:join' cloudA | (UID ; KeyA) if UID == UserY && KeyA == TicketKey
=> < cloudA | DeviceX : ('owner': (UserY, UserX) , 'tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > .

< cloudA | DeviceX : ('tickets': (('key': KeyA, 'time': TimeA), ...) , ...) > if CurrentTime > TimeA + 2
=> < cloudA | DeviceX : ('tickets': (...) , ...) > .

< UserX | 'knowledge': SetX , ... > $ cloudA 'sendKey' UserX | KeyA
=> < UserX | 'knowledge': (SetX, KeyA) , ... > .

< UserX | 'knowledge': SetX , ... > $ cloudA 'sendUID' UserX | UID
=> < UserX | 'knowledge': (SetX, UID) , ... > .
        '''
        code = '''
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
        code = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .

< UserX | 'localTo': DeviceY , ... > $ UserX 'leaves' DeviceY
=> < UserX | 'localTo': nils , ... > .

< DeviceY | ... > $ UserX 'pressButton' DeviceY
=> < DeviceY | ... > $ DeviceY 'callAPI:setKey' cloudA | FreshSecretA .

< cloudA | DeviceY : ('tickets' : SetX , ...) > $ DeviceY 'callAPI:setKey' cloudA | KeyA
=> < cloudA | DeviceY : ('tickets' : (SetX, ('key' : KeyA, 'time' : CurrentTime)), ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...), ...) > $ UserX 'callAPI:getKey' cloudA | DeviceY if CurrentTime < TimeA + 1
=> < cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...), ...) > $ cloudA 'sendKey' UserX | KeyA .

< cloudA | DeviceY : ('owner' : nils, 'tickets' : (('key' : KeyA, ...), ...), ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) //sadasdsd
=> < cloudA | DeviceY : ('owner' : (UserX), 'tickets' : (('key' : KeyA, ...), ...), ...) > .

< cloudA | DeviceY : ('owner' : (UserY), 'tickets' : (('key' : KeyA, ...), ...), ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY), 'tickets' : (('key' : KeyA, ...), ...), ...) > $ cloudA 'sendUID' UserX | UserY .

< cloudA | DeviceY : ('owner' : (UserY), 'tickets' : (('key' : KeyA, ...), ...), ...) > $ UserX 'callAPI:join' cloudA | (UserY ; KeyA)
=> < cloudA | DeviceY : ('owner' : (UserY, UserX), 'tickets' : (('key' : KeyA, ...), ...), ...) > .

< cloudA | DeviceY : ('tickets' : (('key' : KeyA, 'time' : TimeA), ...), ...) > if CurrentTime > TimeA + 2
=> < cloudA | DeviceY : ('tickets' : (...), ...) > .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendKey' UserX | KeyA
=> < UserX | 'knowledge' : (SetX, KeyA) , ... > .

< UserX | 'knowledge' : SetX , ... > $ cloudA 'sendUID' UserX | UIDY
=> < UserX | 'knowledge' : (SetX, UIDY) , ... > .
        '''
        code2 = '''\
< cloudA | DeviceX : ('tickets' : SetA , ...) > $ UserX 'callAPI:getKey' cloudA | DeviceX
=> < cloudA | DeviceX : ('tickets' : SetA , ...) $ cloudA 'send' UserX | KeyB if CurrentTime < Time + 1 .
        '''
        print(checkPolicy(code))
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
        print(checkProp(code))
    def testTransitions():
        code = '''\
< UserX | 'localTo' : DeviceY , ... > => ev1(UserX, DeviceY) .
< UserX | 'localTo' : DeviceY , ... > => ev2(UserX, DeviceY) .
< UserX | 'knowledge' : (KeyA , [Set]) , ... > => ev3(UserX, DeviceY, KeyA) .
< UserX | 'knowledge' : (KeyA , [Set]) , 'UID' : UIDX , ... > => ev4(UserX, UIDX, KeyA) .
< UserX | 'localTo' : DeviceY , ... > => ev5(UserX, DeviceY) .
< UserX | 'localTo' : nils , ... > => ev6(UserX, DeviceY) .
        '''
        print(checkTransitions(code))
    test2()
    #testTransitions()

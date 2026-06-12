#!/bin/python3
from lark import Lark, Transformer,Token
from DSLSyntax import ParseGrammar
import pdb
from copy import deepcopy

def ASTReplace(source,target,repl):
    '''
    replace `target` from `source` with `repl`
    return `True` if replacement happens, else `False`
    Only considering one more layer: the list case
    '''
    for k,v in source.__dict__.items():
        if v == target:
            #print('transform eq',target)
            source.__dict__[k] = repl
            return True
        elif isinstance(v,list) or isinstance(v,tuple) or isinstance(v,set):
            result_list = []
            for i in v:
                if i == target:
                    result_list.append(repl)
                else:
                    result_list.append(i)
            if isinstance(v,tuple):
                result_list = tuple(result_list)
            elif isinstance(v,set):
                result_list = set(result_list)
            source.__dict__[k] = result_list
            return True
    return False

class AST:
    def __init__(self):
        self.parent:AST|None = None
    def __str__(self):
        return self.__repr__()
    def __hash__(self):
        return hash(tuple(self.__dict__))
    def __eq__(self,other):
        if self.__class__ == other.__class__:
            #if self.__dict__ == other.__dict__:
            if self.__dict__ and other.__dict__:
                l = {k:v for k,v in self.__dict__.items() if k != 'parent'}
                r = {k:v for k,v in other.__dict__.items() if k != 'parent'}
                if l == r:
                    return True
        return False
    def visit(self, conditionAndTransforms = [(lambda x: False, lambda x:x)], last=None):
        '''
        find some AST element that matches some conditions, and access the element.
        last: points to the parent object in the last function call
        recursively search through list and tuple
        '''
        for condition,transform in conditionAndTransforms:
            if condition(self):
                if last:
                    ASTReplace(last,self,transform(self))
        for k,v in self.__dict__.items():
            if k == 'parent':
                continue
            if v:
                if isinstance(v,list) or isinstance(v,tuple):
                    for i in v:
                        if 'visit' in dir(i):
                            i.visit(conditionAndTransforms,self)
                else:
                    if 'visit' in dir(v):
                        #print('visit else',type(self),k,v)
                        v.visit(conditionAndTransforms,self)

    def constructIndex(self, parent = None):
        #walk through all childrens, add construct their parent indexes
        self.parent = parent
        for k,v in self.__dict__.items():
            if k == 'parent':
                continue
            if v:
                if isinstance(v,list) or isinstance(v,tuple):
                    for i in v:
                        if 'constructIndex' in dir(i):
                            i.constructIndex(self)
                else:
                    if 'constructIndex' in dir(v):
                        v.constructIndex(self)

    def bloodline(self)->tuple:
        if self.parent:
            return (self.parent, *self.parent.bloodline())
        return ()

class TYPE(AST):#meta type, no use in specifications 
    def __init__(self,v):
        self.v = v# e.g., BOOL , PRINCIPAL , QID
        super().__init__()
    def __repr__(self):
        return '['+self.v+']'
    def __str__(self):
        return '['+self.v+']'
                  
class DOTS(AST): 
    init_num = 2
    def __init__(self, dots_num = 2):
        self.dots_num = dots_num
    def __repr__(self):
        return '.'*self.dots_num

class NILS(AST):
    def __repr__(self):
        return 'nils'
class VARIABLE(AST):
    def __init__(self,i,type_=None):
        super().__init__()
        self.ident = i
        self.type_ = type_
    def __repr__(self):
        return self.ident
class QID(AST):
    def __init__(self,i):
        super().__init__()
        self.ident = i
    def __repr__(self):
        #return "'"+self.ident+"'"
        return self.ident
class PAIR(AST):
    def __init__(self,k,v):
        super().__init__()
        self.k = k
        self.v = v
    def __repr__(self):
        return f'{self.k} : {self.v}'

def fixpoint(last,f):
    #f should not modify i
    while True:
        new = f(last)
        if new == last:
            break
        else:
            last = new
    return new

class SET_bak(AST):
    def __init__(self,*tup):
        super().__init__()
        self.v:set = set(tup)
    def binary(self):
        return isinstance(self.v,set) and len(self.v) == 2
    def add(self,item):
        self.v.add(item)
        return self
    def has(self,item):
        return item in self.v
    def hasType(self, type_):
        for i in self.v:
            if isinstance(i, type_):
                return True
        return False

    def getByType(self, type_):
        for i in self.v:
            if isinstance(i, type_):
                return i
        return None

    def remove(self,item):
        self.v.discard(item)
        return self 

    def removeByType(self,type_):
        l = []
        for i in self.v:
            if not isinstance(i,type_):
                l.append(i)
        self.v = set(l)
        return self

    def keys(self):
        return [i.k for i in self.v if isinstance(i,PAIR)]

    def update(self,idx,v):
        l = list(self.v)
        l[idx] = v
        self.v = set(l)
        return self.v

    def get(self,k)->PAIR|None:
        for i in self.v:
            if isinstance(i,PAIR) and i.k == k:
                return i
        return None

    def vals(self,k):
        for i in self.v:
            if isinstance(i,PAIR) and i.k == k:
                return i.v
        return None
    def __repr__(self):
        return f'SET{self.v}'
    def __str__(self):
        if len(self.v)>0:
            return '('+' , '.join([str(i) for i in self.v])+')'
        #if len(self.v)>1:
        #    return '('+' , '.join([str(i) for i in self.v])+')'
        #elif len(self.v) == 1:
        #    return str(list(self.v)[0])
        else:
            return 'nils'

    def __copy__(self):
        return SET(*tuple(self.v))

class SET(AST):
    def __init__(self,*tup):
        super().__init__()
        self.v:tuple = tup
        #self.v:set = set(tup)
    def binary(self):
        return isinstance(self.v,tuple) and len(self.v) == 2
    def addIfNo(self,item):
        if len(self.v) == 0:
            self.v = tuple([item])
        else:
            if item not in self.v:
                self.v = (*self.v,item)
    def add(self,item):
        if len(self.v) == 0:
            self.v = tuple([item])
        else:
            self.v = (*self.v,item)
    def has(self,item):
        for i in self.v:
            if i == item:
                return True
        return False
    def hasType(self, type_):
        for i in self.v:
            if isinstance(i, type_):
                return True
        return False

    def getByType(self, type_):
        for i in self.v:
            if isinstance(i, type_):
                return i
        return None

    def remove(self,item):
        v2 = ()
        for i in self.v:
            if i != item:
                v2 = (*v2,i)
        self.v = v2

    def removeOnce(self,item):
        v2 = ()
        first = True
        for i in self.v:
            if first:
                if i != item:
                    v2 = (*v2,i)
                else:
                    first = False
            else:
                v2 = (*v2,i)
        self.v = v2

    def removeByType(self,type_):
        v2 = ()
        for i in self.v:
            if not isinstance(i,type_):
                v2 = (*v2,i)
        self.v = v2
        return self

    def keys(self):
        return [i.k for i in self.v if isinstance(i,PAIR)]
    def update(self,idx,v):
        l = list(self.v)
        l[idx] = v
        self.v = tuple(l)
        return self.v
    def get(self,k)->PAIR|None:
        for i in self.v:
            if isinstance(i,PAIR) and i.k == k:
                return i
        return None
    def vals(self,k):
        for i in self.v:
            if isinstance(i,PAIR) and i.k == k:
                return i.v
        return None
    def __repr__(self):
        return f'SET{self.v}'
    def __str__(self):
        if len(self.v)>0:
            return '('+' , '.join([str(i) for i in self.v])+')'
        #if len(self.v)>1:
        #    return '('+' , '.join([str(i) for i in self.v])+')'
        #elif len(self.v) == 1:
        #    return str(self.v[0])
        else:
            return 'nils'
    def __copy__(self):
        return SET(*self.v)
    
    @staticmethod
    def containOrContained(s1,s2):
        set1 = set(s1.v)
        set2 = set(s2.v)
        set3 = set1.intersection(set2) 
        return set3 == set1 or set3 == set2
    
    @staticmethod
    def disduplicate(s1):
        set1 = set(s1.v)
        s1.v = tuple(set1)
        return s1
def normalize(att:SET):
    #return att
    '''
SET[SET[A],B,...] => SET[A,B]
    '''
#one item the same, handle inside, two more items, check the first, up one level
#SET(DeviceB : SET(SET(SET(SET(A,), B), C), D),)
#SET(SET(SET(SET(A,), B), C), D)
#SET(SET(SET(A,), B), C, D)
#SET(SET(A,), B, C, D)
#SET(A, B, C, D)
    def helper(l):
        #pdb.set_trace()
        if isinstance(l,PAIR):
            return PAIR(l.k,helper(l.v))
        elif isinstance(l,SET):
            if len(l.v) > 1:# two more items
                #pdb.set_trace()
                if isinstance(l.v[0],SET):
                    return SET(*l.v[0].v,*l.v[1:])
                else:
                    return SET(helper(l.v[0]),*l.v[1:])
            else:#one item
                return SET(helper(l.v[0]))
        return l
    return fixpoint(att,helper)

class CHOICES(SET):#meta type
    def __init__(self,*tup):
        super().__init__(*tup)
    def makeFromSet(s:SET):
        return CHOICES(*s.v)
    def __repr__(self):
        return f'CHOICES{self.v}'
    def __str__(self):
        if len(self.v)>1:
            return '{'+' , '.join([str(i) for i in self.v])+'}'
        elif len(self.v) == 1:
            return str(self.v[0])
        else:
            return 'nils'

class LIST(AST):
    def __init__(self,v:list):
        super().__init__()
        self.v = v
    def binary(self):
        return len(self.v) == 2
    def __repr__(self):
        return f'LIST{self.v}'
    def __str__(self):
        return '('+' ; '.join([str(i) for i in self.v])+')'
class BOOL(AST):
    def __init__(self,v):
        super().__init__()
        self.v = v
    def __repr__(self):
        if self.v:
            return 'true'
        else:
            return 'false'


class INFIX_EXP(AST):
    def __init__(self,lhs,op,rhs):
        super().__init__()
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    def __repr__(self):
        return f"{self.lhs} {self.op} {self.rhs}"

class CONDITION(INFIX_EXP):
    def __init__(self,lhs,op,rhs):
        super().__init__(lhs,op,rhs)

class ARITH(INFIX_EXP):
    def __init__(self,lhs,op,rhs):
        super().__init__(lhs,op,rhs)

class FUNCALL(AST):
    def __init__(self,funcname:str,params:list):
        super().__init__()
        self.funcname = funcname
        self.params = params
    def __repr__(self):
        params_s = ', '.join([param.__repr__() for param in self.params])
        return f'{self.funcname}({params_s})'

class EVENT_NAME(FUNCALL):
    def __init__(self,funcname:int,params):
        fn = 'ev'+str(funcname)
        super().__init__(fn,params)
        self.event = None

class EVENT(AST):
    def __init__(self,i0,i1,i2,i3=None):
        super().__init__()
        self.subject = i0
        self.action = i1
        self.object = i2
        self.arguments = i3

    def __repr__(self):
        if self.arguments:
            return f'$ {self.subject} {self.action} {self.object} | {self.arguments}'
        else:
            return f'$ {self.subject} {self.action} {self.object}'
    def __eq__(self,other):
        if self.__class__ == other.__class__:
            return variableNormalize(self) == variableNormalize(other)
        return False
    def __hash__(self):
        return hash(variableNormalize(self))

def variableNormalize(evt:EVENT)->str:
    # return a string that after normalize vairable names
    nameMap = {}
    typeVarCnt = {}
    replaces = []
    def rename(i):
        if isinstance(i,VARIABLE):
            if i.type_ not in typeVarCnt:
                typeVarCnt[i.type_] = 1
            if i.ident not in nameMap:
                try:
                    nameMap[i.ident] = i.type_+str(typeVarCnt[i.type_])
                except:
                    pdb.set_trace()
                typeVarCnt[i.type_] += 1
            replaces.append((i.ident,nameMap[i.ident]))
        elif isinstance(i, LIST):
            for ii in i.v:
                rename(ii) 
    rename(evt.subject)
    rename(evt.action)
    rename(evt.object)
    rename(evt.arguments)
    rst = str(evt)
    for o,n in replaces:
        rst = rst.replace(o,n)
    return rst

class PRINCIPAL(AST):
    def __init__(self,type_,i:str):
        super().__init__()
        self.type_ = type_
        self.ident = i
    def __repr__(self):
        return self.ident

#class ATTRIBUTES(AST):
#    def __init__(self, pairs:list[PAIR], dots:DOTS = None):
#        super().__init__()
#        self.pairs = pairs
#        self.dots = dots
#    def __repr__(self):
#        l = []
#        l += [str(pair) for pair in self.pairs]
#        if self.dots:
#            l.append(str(self.dots))
#        return ' , '.join(l)

class INTERNAL_STATE(AST):
    def __init__(self,p:PRINCIPAL,a:SET|None=None):
        super().__init__()
        self.principal = p
        self.attributes = a
    def __repr__(self):
        if not self.attributes:
            a = ''
        else:
            a = str(self.attributes)
        return f'< {self.principal} | {a} >'

class STATE_RULE(AST):
    def __init__(self,lhs:list,rhs:list,condition=None):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.condition = condition

    def __repr__(self):
        lhs = ' '.join([str(i) for i in self.lhs])
        rhs = ' '.join([str(i) for i in self.rhs])
        if self.condition:
            return f'ceq {lhs} \n= {rhs} if {self.condition} .'
        else:
            return f'eq {lhs} \n= {rhs} .'
    def __get(self, field:str, p:PRINCIPAL)->INTERNAL_STATE|None:
        for is_or_e in self.__dict__[field]:
            if isinstance(is_or_e, INTERNAL_STATE):
                istate = is_or_e
                if istate.principal == p:
                    return istate
        return None
    def lhsGet(self,p:PRINCIPAL)->INTERNAL_STATE|None:
        return self.__get('lhs',p)
    def rhsGet(self,p:PRINCIPAL)->INTERNAL_STATE|None:
        return self.__get('rhs',p)

class EVENT_DECL(AST):
    def __init__(self,ref:str, event:EVENT, params:list[VARIABLE]):
        self.ref = ref
        self.event = event
        self.params = params
    
    def __repr__(self):
        if len(self.params) > 0:
            params = ', '.join([str(var) for var in self.params])
            return f'eq {self.ref}({params}) = '+str(self.event)+' .'
        else:
            return f'eq {self.ref} = '+str(self.event)+' .'

    def typeDecl(self, vtypes:dict[str,str]):
        types = [vtypes[var.ident] for var in self.params]
        return ' '.join(['ops', self.ref, ':', ' '.join(types),'->','Event','.'])

class EVENT_RULE(AST):
    def __init__(self,lhs:list,rhs:EVENT_NAME):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
    def __str__(self):
        lhs = ' '.join([str(i) for i in self.lhs])
        rhs_ast = deepcopy(self.lhs)
        #in event rule, time automatically increment in rhs
        for istate in rhs_ast:
            if isinstance(istate.principal,PRINCIPAL):
                if istate.principal.ident == 'system':
                    if pair := istate.attributes.get(QID("'time'")):
                        pair.v = ARITH(VARIABLE('N','Nat'),'+','1')
        rhs = ' '.join([str(i) for i in rhs_ast])
        event = self.rhs
        name = self.rhs.funcname
        return f'rl [r{name}]: E @ S {lhs} \n=> ep: {event} @ S {rhs} .'

class PROPOSITION(AST):
    def __init__(self, propname:str, constraint:INTERNAL_STATE|EVENT):
        super().__init__()
        self.propname = propname
        self.constraint = constraint
        #self.constraints = constraints
    def __repr__(self):
        return f"{self.propname} =| {self.constraint}"

    def __str__(self):
        atLeastOneEvent = False
        istates = []
        events = []
        eventConstraints = []
        #for constraint in self.constraints:
        if isinstance(self.constraint, INTERNAL_STATE):
            istates.append(self.constraint)
        elif isinstance(self.constraint, EVENT):
            events.append(self.constraint)
            atLeastOneEvent = True
        else:
            print('[-] ERROR',type(self.constraint))
            print(self.constraint)
            exit(1)
        if atLeastOneEvent:
            prefix = 'ceq'
            for evt in events:
                if isinstance(evt.subject, PRINCIPAL):
                    eventConstraints.append(f'subject(E) == {evt.subject}')
                if isinstance(evt.action, QID):
                    eventConstraints.append(f'action(E) == {evt.action}')
                if isinstance(evt.object, PRINCIPAL):
                    eventConstraints.append(f'object(E) == {evt.object}')
            if len(eventConstraints) == 0:
                print('[-] Warning: propotision constraint bad, need check:',self.constraint)
                eventConstraints.append('true')
            suffix = 'if '+' and '.join([str(ec) for ec in eventConstraints])
        else:
            prefix = 'eq'
            suffix = ''
        return f'{prefix} E @ S '+' '.join([str(i) for i in istates])+f" |= {self.propname} = true "+suffix+" ."

class INIT(AST):
    def __init__(self, istates:list[INTERNAL_STATE]):
        self.istates = istates
    def __repr__(self):
        return ' '.join([str(istate) for istate in self.istates])

class DSL(AST):
    def __init__(self, rules:list[STATE_RULE|EVENT_RULE]):
        self.rules = rules
    def __repr__(self):
        return '\n'.join([str(rule) for rule in self.rules])


# Define a transformer to convert the parse tree into Python data structures
class DSLBaseTransformer(Transformer):
    def __init__(self,varmap = {}):
        self.varmap = varmap
        super().__init__()

    def state_rule(self, items):
        if len(items) > 2:
            return STATE_RULE(items[0], items[1],items[2])
        else:
            return STATE_RULE(items[0], items[1])

    def event_rule(self, items):
        return EVENT_RULE(items[0:-1], items[-1])

    def proposition(self, items):
        return PROPOSITION(items[0], items[1])

    def event_name(self, items):
        return EVENT_NAME(items[0], items[1:])

    def condition(self,items):
        return CONDITION(items[0],items[1],items[2])

    def arith(self,items):
        if len(items) == 1:
            return items[0]
        elif isinstance(items[0],Token) and str(items[0].children[0]) == '(':
            return items[1]
        else:
            return ARITH(items[0],items[1],items[2])

    def logical_state(self, items):
        return items

    def internal_state(self, items):
        if len(items) > 1:
            return INTERNAL_STATE(items[0], items[1])
        else:
            return INTERNAL_STATE(items[0])

    def event(self, items):
        if len(items) == 4:
            return EVENT(items[0], items[1], items[2], items[3])
        else:
            return EVENT(items[0], items[1], items[2])

    def principal(self, items):
        return items[0]

    def PRIN(self, items):
        return PRINCIPAL("Principal", str(items))

    def USER(self, items):
        return PRINCIPAL("User", str(items))

    def DEVICE(self, items):
        return PRINCIPAL("Device", str(items))

    def CLOUD(self, items):
        return PRINCIPAL("Cloud", str(items))

    def APP(self, items):
        return PRINCIPAL("App", str(items))

    def SERVER(self, items):
        return PRINCIPAL("Server", str(items))

    def CLIENT(self, items):
        return PRINCIPAL("Client", str(items))

    def pair(self, items):
        return PAIR(items[0], items[1])

    def item(self, items):
        return items[0]

    def list(self, items):
        #return ("list", items)
        return LIST(items)

    def set(self, items):
        if len(items) == 1 and isinstance(items[0],NILS):
            return NILS()
        #else:
        return SET(*tuple(items))

    def arguments(self, items):
        return items[0]

    def attributes(self, items):
        #if isinstance(items[-1], DOTS):
        #    return ATTRIBUTES(items[0:-1],items[-1])
        #else:
        #    return ATTRIBUTES(items)
        if len(items) == 1 and isinstance(items[0],SET):
            return items[0]
        return SET(*items)
        #return normalize(SET(items))
        #return normalize(items[0])

    def action(self, items):
        return items[0]
    
    def funcall(self,items):
        return FUNCALL(items[0],items[1:])

    def qid(self, items):
        i = items[0]
        if isinstance(i,VARIABLE):
            return i
        else:
            return QID(i)

    def number(self, items):
        '''
        simple unpack it, to avoid Tree[...]
        '''
        return items[0]

    def STRING(self,items):
        return str(items)

    def INTEGER(self,items):
        return int(items)

    def VARIABLE(self,items):
        if str(items) not in self.varmap:
            vtype = None
        else:
            vtype = self.varmap[str(items)]
        return VARIABLE(str(items),vtype)

    def BOOL(self,items):
        if str(items) == 'true':
            return BOOL(True)
        else:
            return BOOL(False)

    def DOTS(self,items):
        return DOTS()
    def NILS(self,items):
        return NILS()
        #return SET()
class DSLTransformer(DSLBaseTransformer):
    def start(self, items):
        return DSL(items)

class DSLInitTransformer(DSLBaseTransformer):
    def start(self, items)->INIT:
        return INIT(items)

class ASTVisitor():
    def visitSubject(self,i, last):
        return str(i)
    def visitAction(self,i, last):
        return str(i)
    def visitObject(self,i, last):
        return str(i)
    def visitArgument(self,i, last):
        return str(i)
    def visitPrincipal(self,i, last):
        return str(i)
    def visitAttribute(self,i, last):
        return str(i)
    def visitEventName(self, i, last):
        return str(i)

    def visitEvent(self,i, last):
        self.visitSubject(i.subject, i)
        self.visitAction(i.action, i)
        self.visitObject(i.object, i)
        self.visitArgument(i.arguments, i)

    def visitCondition(self,i, last):
        return str(i)

    def visitInState(self,i, last):
        self.visitPrincipal(i.principal, i)
        self.visitAttribute(i.attributes, i)

    def visitLogicalState(self,i, last):
        if isinstance(i, INTERNAL_STATE):
            self.visitInState(i, last)
        elif isinstance(i, EVENT):
            self.visitEvent(i, last)
        else:
            print('[-] unexptected type:', type(i))
    
    def visitStateRule(self,child):
        for i in child.lhs:
            self.visitLogicalState(i, child)
        for i in child.rhs:
            self.visitLogicalState(i, child)
        if child.condition:
            self.visitCondition(child.condition, child)

    def visitEventRule(self,child):
        for i in child.lhs:
            self.visitInState(i, child)
        self.visitEventName(child.rhs, child)
    
    def visitProposition(self,child):
        i = child.constraint
        if isinstance(i, INTERNAL_STATE):
            self.visitInState(i, child)
        elif isinstance(i, EVENT):
            self.visitEvent(i, child)
        else:
            print('[-] unexptected type:', type(i))

    def visitInit(self, init):
        for istate in init.istates:
            self.visitInState(istate, init)

    def visit(self, dsl):
        if isinstance(dsl, INIT):
           self.visitInit(dsl)
        else:
            for rule in dsl.rules:
                if isinstance(rule, STATE_RULE):
                    self.visitStateRule(rule)
                elif isinstance(rule, EVENT_RULE):
                    self.visitEventRule(rule)
                elif isinstance(rule, PROPOSITION):
                    self.visitProposition(rule)

def parseAST(code:str, varmap:dict={})->DSL:
    parser = Lark(ParseGrammar.dsl_grammar, parser='earley')
    transformer = DSLTransformer(varmap)
    tree = parser.parse(code)
    ast = transformer.transform(tree)
    return ast

def parseInitAST(code:str):
    parser = Lark(ParseGrammar.init_grammar, parser='earley')
    transformer = DSLInitTransformer()
    tree = parser.parse(code)
    ast = transformer.transform(tree)
    return ast

def parsePropAST(code:str,varmap:dict={})->DSL:
    return parseAST(code,varmap)
    

if __name__ == '__main__':
    def testFixPoint():
        a= [1,2,3,4,5,6]
        def f(l):
            if sum(l) > 10:
                l = l[:-1]
            return l
        print(fixpoint(a,f))

    #testFixPoint()
    a = PAIR(QID('time'),TYPE('Int'))
    b = PAIR(QID('time'),TYPE('Int'))
    print(a==b)

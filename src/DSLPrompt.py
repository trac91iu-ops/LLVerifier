#!/bin/python3
StateRule = '''\
<StateRule> ::= <LogicalState> "=>" <LogicalState> "."
<LogicalState> ::= <InternalState>+ <Event>?\
'''

EventDecl = '''\
<EventDeclare> ::= "eq" <EventName> "=" <Event>  "."
<EventName> ::= "ev" integer "(" <Var> ("," <Var>)* ")"\
'''

EventRule = f'''\
<EventRule> ::= <InternalState>* "=>" <EventName> "."
{EventDecl}\
'''

Init = '''\
<InitState> ::= <InternalState>+\
'''

VarDecl = '''\
<VarDef> ::= "vars" <Var>+ ":" <Type> "."\
'''

Base= '''\
<InternalState> ::= "< " <Principal> " | " <Attributes> " >"
<Event> ::= "$ " <Principal> <Action> <Principal> (" | " <Arguments>)?
<Var> ::= /A-Z/ Identifier
<Principal> ::= <User> | <Device> | <Cloud> | <App> | <Server> | <Client> | <Var>
<Pair> ::= <Qid>  ":" <Item> | <Qid> ":" <Set> |  <Principal> ":" <Set>
<Item> ::= Bool | <Qid> | integer | <Principal> | <Pair> | <Var>
<List> ::= "(" <Item> (";" <Item>)* ")" 
<Set> ::=  "(" <Item> ("," <Item>)* ")" | "nils"
<Arguments> ::= <Item> | <List> 
<Attributes> ::= <Pair> ("," <Pair>)* ("," "...")? | "..."
<Action> ::= <Qid>
<Qid> ::= "'" Identifier "'"
<User> ::= "user" Identifier
<Device> ::= "device" Identifier
<Cloud> ::= "cloud" Identifier
<App> ::= "app" Identifier
<Server> ::= "server" Identifier
<Client> ::= "client" Identifier
Identifier ::= /[a-zA-Z0-9_:]+/\
'''

BaseBak= '''\
<InternalState> ::= "< " <Principal> " | " <Attributes> " >"
<Event> ::= "$ " <Principal> <Action> <Principal> (" | " <Arguments>)?
<Var> ::= /A-Z/ Identifier
<Principal> ::= <User> | <Device> | <Cloud> | <App> | <Server> | <Client> | <Var>
<Pair> ::= <Qid>  ":" <Item> | <Principal> ":" <Item>
<Item> ::= Bool | <Qid> | integer | <Principal> | <Pair> | <Var>
<List> ::= <Item> ";" <List> | <Item>
<Set> ::=  <Item> "," <Set> | <Item> | "nils" | "..."
<Arguments> ::= <List>
<Attributes> ::= <Set>
<Action> ::= <Qid>
<Qid> ::= "'" Identifier "'"
<User> ::= "user" Identifier
<Device> ::= "device" Identifier
<Cloud> ::= "cloud" Identifier
<App> ::= "app" Identifier
<Server> ::= "server" Identifier
<Client> ::= "client" Identifier
Identifier ::= /[a-zA-Z0-9_:]+/\
'''

Condition = '''\
<CS> ::= <LogicalState> "=>" <LogicalState> "if" <Condition> "."
<Condition> ::= <Arith> <CMP> <Arith>
<Arith> ::= <Arith> <OP> <Arith> | integer | <Var>
<OP> ::= "+" | "-" | "*"
<CMP> ::= ">" | "<" | ">=" | "<=" | "==" | "=/="\
'''

Types = '''\
<Type> ::= "Qid" | "Bool" | "Nat"| "Principal" |  "User"
         | "Device" | "Cloud" | "App" | "Server" | "Client"
         | "Set" | "List" | "Event" | "Action"\
'''

Template = '''\
<Pair> ::= (<Qid> | <Principal>)  ":" (<Item> | <Choices>)
<Choices> ::= "{" <Placeholder> ("," <Placeholder>)* "}"
<Placeholder> ::= "[" <Type> "]" | Item\
'''

Proposition2 = '''\
<Proposition> ::= <PropName> "=|" <Constraint> "."
<Constraint> ::= <InternalState> | <Event>
'''

Proposition = '''\
<Proposition> ::= <StateProp> | <EventProp> 
<StateProp> ::= "eq E @ S" <InternalState> "|=" <PropName> "= true ."
<EventProp> ::= "ceq E @ S |=" <PropName> " = true if sd(E) == sd(" (<EventName>) ") ." 
	| "ceq E @ S |=" <PropName> " = true if " ("subject" | "object") "(E) == " <Principal> " ."
<EventName> ::= "ev" Integer "(" <Params> ')'
<Params> ::= <Param> ("," <Param>)*\
'''
#TODO: resolve the collision with rule EventDecl

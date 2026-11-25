#!/bin/python3
# Kept consistent with DSLSyntax.ParseGrammar (the parser behind every syntax check);
# tests/test_model_pipeline.py checks the examples below against the parser.
StateRule = '''\
<StateRule> ::= <LogicalState> "=>" <LogicalState> ("if" <Condition>)? "."
<LogicalState> ::= <InternalState>+ <Event>? <InternalState>*\
'''

EventDecl = '''\
<EventDeclare> ::= "eq" <EventName> "=" <Event>  "."
<EventName> ::= "ev" integer "(" <Item> ("," <Item>)* ")"   (* at least one argument *)\
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
<InternalState> ::= "<" <Principal> "|" <Attributes>? ">"
<Event> ::= "$" <Principal> <Action> <Principal> ("|" <Arguments>)?
<Principal> ::= <User> | <Device> | <Cloud> | <App> | <Server> | <Client> | <Var>
<Attributes> ::= (<Pair> | "...") ("," (<Pair> | "..."))* | <Set>
<Pair> ::= <Qid> ":" <Item> | <Principal> ":" "(" <Attributes> ")"
<Item> ::= <Bool> | <Qid> | integer | <Principal> | <Pair> | <Set> | <FunCall> | "..."
<Set> ::= "nils" | "(" <Item> ("," <Item>)* ")"
<List> ::= "(" <Item> (";" <Item>)* ")"
<FunCall> ::= ("encrypt" | "decrypt") "(" <Item> ("," <Item>)* ")" | "list" <List>
<Arguments> ::= <Item> | <List>
<Action> ::= <Qid> | <Var>
<Qid> ::= /'[^']*'/
<Bool> ::= "true" | "false"
<Var> ::= /[A-Z][a-zA-Z0-9_]*/
<User> ::= "user" /[A-Z][a-zA-Z0-9_]*/
<Device> ::= "device" /[A-Z][a-zA-Z0-9_]*/
<Cloud> ::= "cloud" /[A-Z][a-zA-Z0-9_]*/
<App> ::= "app" /[A-Z][a-zA-Z0-9_]*/
<Server> ::= "server" /[A-Z][a-zA-Z0-9_]*/
<Client> ::= "client" /[A-Z][a-zA-Z0-9_]*/
(* A principal key always takes a parenthesized value: `DeviceX : ('key' : K , ...)`,
   `UserX : ((UserY , Rest))` for a set, `UserX : (nils)` when empty. *)
(* In <Arguments>, `;` separates ordered arguments; `(A , B)` is one set-valued argument. *)\
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
<Condition> ::= <Arith> <CMP> <Arith>   (* exactly one comparison; no "and"/"or" *)
<Arith> ::= <Arith> <OP> <Arith> | "(" <Arith> ")" | integer | <Var> | <FunCall> | "nils"
<OP> ::= "+" | "-" | "*" | "/"
<CMP> ::= ">" | "<" | ">=" | "<=" | "==" | "=/="\
'''

# Same sorts as the variable-type validator in LLMInterface._variableTypes.
Types = '''\
<Type> ::= "Qid" | "Bool" | "Nat" | "Principal" | "User"
         | "Device" | "Cloud" | "App" | "Server" | "Client"
         | "Set" | "List" | "Item" | "Key" | "Action" | "Arguments" | "Attributes"\
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

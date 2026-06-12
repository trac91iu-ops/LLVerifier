#!/bin/python3
PrinTypes = ['User', 'Device', 'Server', 'Client', 'App', 'Principal', 'Cloud']
class ParseGrammar:
    #1. More loose grammar to parse code, give a chance to manipulate AST to fix
    #2. More simpler AST for algorithm to operate
    #ParseGrammar is a super set of CheckGrammar
    # Define the grammar for Les
    dsl_base = """\
    state_rule: logical_state "=>" logical_state ("if" condition)? " ."

    event_rule: internal_state* "=>" event_name " ." 

    proposition: STRING "=|" (internal_state | event) " ."

    event_decl: "eq" event_name "=" event " ."

    event_name: "ev" number "(" item ("," item)* ")"

    condition: arith CMP arith

    arith: arith OP arith | "(" arith ")" |  number | funcall | NILS

    number: INTEGER | VARIABLE
    
    OP: "+" | "-" | "*" | "/" 
    CMP: ">" | "<" | ">=" | "<=" | "==" | "=/="

    logical_state: internal_state+ event? internal_state*

    internal_state: "<" principal "|" attributes ">" | "<" principal "|" ">"

    event: "$" principal action principal ("|" arguments)?

    principal.1: USER | DEVICE | CLOUD | APP | SERVER | CLIENT | VARIABLE

    USER: "user" /[A-Z][a-zA-Z0-9_]*/
    DEVICE: "device" /[A-Z][a-zA-Z0-9_]*/
    CLOUD: "cloud" /[A-Z][a-zA-Z0-9_]*/
    APP: "app" /[A-Z][a-zA-Z0-9_]*/
    SERVER: "server" /[A-Z][a-zA-Z0-9_]*/
    CLIENT: "client" /[A-Z][a-zA-Z0-9_]*/

    pair: qid ":" item | principal ":" "(" attributes ")"

    item: BOOL | qid | INTEGER | principal | pair | DOTS | funcall | VARIABLE | set

    funcall: FUNCNAME "(" item ("," item)* ")"

    FUNCNAME: "encrypt" | "decrypt"

    list: "(" item (";" item)* ")" | item

    set: NILS | "(" item ("," item)* ")" 

    arguments: list

    attributes: (pair | DOTS) ("," (pair | DOTS))* |  set
    action: qid | VARIABLE

    qid.2: /'[^']*'/ 

    BOOL: "true" | "false"
    NILS: "nils"
    DOTS: "..."/\\./* 
    VARIABLE: /[A-Z]//[a-zA-Z0-9_]/* 

    STRING: /[a-zA-Z0-9_:]+/
    INTEGER: /[0-9]+/

    %import common.WS
    %ignore WS
"""
#arith: arith OP arith | "(" arith ")" | number | NILS
#attributes: pair ("," pair)* ("," DOTS)? | DOTS | set

    init_grammar = '''\
start: internal_state+
'''+dsl_base

    dsl_grammar = """\
start: (state_rule | event_rule | proposition)+
"""+dsl_base

class CheckGrammar:
#use a more restrict grammar to show error message, allowing LLM to revise
# Define the grammar for Les
#logical_state: internal_state+  event?
#logical_state: (internal_state | event)*
#the approach of proposition below performs worse
    dsl_base = """\
    state_rule: logical_state "=>" logical_state ("if" condition)? " ."

    event_rule: internal_state* "=>" event_name " ." 

    proposition: STRING "=|" (internal_state | event) " ."

    event_decl: "eq" event_name "=" event " ."

    event_name: "ev" number "(" item ("," item)* ")"

    condition: arith CMP arith

    arith: arith OP arith | "(" arith ")" | number | NILS

    number: INTEGER | VARIABLE
    
    OP: "+" | "-" | "*" | "/" 
    CMP: ">" | "<" | ">=" | "<=" | "==" | "=/="

    logical_state: internal_state+ event? internal_state*

    internal_state: "<" principal "|" attributes ">" | "<" principal "|" ">"

    event: "$" principal action principal ("|" arguments)?

    principal.1: USER | DEVICE | CLOUD | APP | SERVER | CLIENT | VARIABLE

    USER: "user" /[A-Z][a-zA-Z0-9]*/
    DEVICE: "device" /[A-Z][a-zA-Z0-9]*/
    CLOUD: "cloud" /[A-Z][a-zA-Z0-9]*/
    APP: "app" /[A-Z][a-zA-Z0-9]*/
    SERVER: "server" /[A-Z][a-zA-Z0-9]*/
    CLIENT: "client" /[A-Z][a-zA-Z0-9]*/

    pair: qid ":" item | principal ":" "(" attributes ")"

    item: BOOL | qid | INTEGER | principal | pair | DOTS | funcall | VARIABLE | set

    funcall: FUNCNAME "(" item ("," item)* ")"

    FUNCNAME: "encrypt" | "decrypt"

    list: "(" item (";" item)* ")" | item

    set: NILS | "(" item ("," item)* ")" 

    arguments: list | item

    attributes: pair ("," pair)* ("," DOTS)? | DOTS | set

    action: qid | VARIABLE

    qid.2: /'[^']*'/ 

    BOOL: "true" | "false"
    NILS: "nils"
    DOTS: "..."/\\./* 
    VARIABLE: /[A-Z]//[a-zA-Z0-9_]/* 

    STRING: /[a-zA-Z0-9_:]+/
    INTEGER: /[0-9]+/

    %import common.WS
    %ignore WS
"""
#attributes: "(" pair ("," pair)* ("," DOTS)? | DOTS "?"
# qid.2: "'" STRING "'" 
# attributes: pair ("," pair)* ("," DOTS)?
# PRIN: STRING 

    init_grammar = '''\
start: internal_state+
'''+dsl_base

    dsl_grammar = """\
start: (state_rule | event_rule | proposition)+
"""+dsl_base

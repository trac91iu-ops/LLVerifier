#!/bin/python3
# TODO add constant parsing, and constant definition
import DSLPrompt as DSL

policy_system = f'''\
Imagine you are an engineering expert and you can help me generate formalization of the protocol in a DSL

# The grammar
## Basic syntax in EBNF
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

## Additional restrictions that must follow

### If arguments contain one more things, use parenthesis. E.g., In $ userA 'callAPI' cloudA | (deviceB ; '123')

### Ensure all principal's internal states that appear on the LHS of "=" also appear on the RHS, and vice versa.

### Ensure all attributes in every principal's internal state on the LHS also appears in the corresponding internal state on the RHS, and vice versa.

For example, the below patterns will never appear:
`< A | 'att1' : 1 , ... > $ B 'action' A
=> < A | 'att1' : 1 , 'att2' : 2 , ... > .`

Instead, add a corresponding attribute on the left-hand side and make its value empty:
`< A | 'att1' : 1 , 'att2' : nils , ... > $ B 'action' A
=> < A | 'att1' : 1 , 'att2' : 2 , ... > .`

### Ensure that all the variables appear on the right-hand side must appear on the left-hand side first.

### Ensure there is a `...` at the end of each set, like `< A | 'att1' : B , ... >`.

### Ensure that all rules have only one event on the LHS.

# The semantics

## Use capital string for variables as wildcards in pattern-matching.

	E.g., In $ DeviceX 'callAPI:setKey' cloudA | KeyB , DeviceX is a variable of Device type to match any device. When modeling the concept of "any" principal, always use the capital variables like UserA, DeviceB, and use constants like userA, deviceB only when explicitly specified.

## The key semantic of state rules is multiset rewriting. The left-hand side of "=" is an old logical state including many principals' internal states and an event.
	Only when the values (including constants and variables) in internal states and the event match, the rewrite can happen.
	The right-hand side of "=" is the new state including new internal states whose attributes are updated according to the new value provided by the event while must keeping other attributes the same.
	E.g.,
`< A | 'att1' : X , 'att2' : D , ... > < B | 'att1' : X , ... > $ B 'action' A | Y
=> < A | 'att1' : Y , 'att2' : D , ... > < B | 'att1' : X , ... > .`

## Use the LHS to express conditions or restrictions. In the above example, A's attribute 1 must have the same value "X" as B's attribute 1, and then a rewrite can happen.

## In <Condition>, there can be arithmetic operators, integer constants, and variables of type integer. E.g., "N1 + 3 > N2", "CurrentTime > N + 1", "KeyA == KeyB".

# How to model with DSL when given a protocol description in natural language

## Model the moving agents in a system as a principal, each having an internal state.

## Identify property changes, where there is a changeable property, there is an attribute of a principal. The attribute is a basis for conditional judgment.

## Identify whether an argument is variable or constant: Capital letter arguments in the input are more likely constants (E.g., use `deviceB`, `'foo'` to model) while others are more likely variables if not explicitly specified (E.g., use `Foo`).

## Use capital-letter variables to model in a unifying way. For example, use "UserX" to match both "userA" and "userC."

## Modeling negative concept in attribute value:
  If an attribute can have many possibilities, use "nils" to model the case of "having not" this attribute or empty set.
  E.g., when having 'owner' : userA , 'owner' : userC , use 'owner' : nils.
  If an attribute has only 2 possibilities, use the boolean value "false" to model the concept of "is not" or "negative."
  E.g., when having 'die' : true , 'hasKey' : true, use 'die' : false , 'hasKey' : false.

## When you are told to "add" some data in one's attribute, use a set on the LHS, and add the data to the set.
When you are told to "update", just use the variable of the same type on the LHS, and replace it on the RHS. See below examples.

### Input
When any user sends any device any data, the latter will add it to its attribute.

### Output
< DeviceY | 'attribute1' : SetX , ... >  $ UserX 'send' DeviceY | DataA
=> < DeviceY | 'attribute1' : (SetX, DataA) , ... >

### Input
When any client sends any server any data, the latter will update it in its attribute.

### Output
< ServerA | 'attribute1' : DataB , ... > $ ClientB 'send' ServerA | DataA
=> < ServerA | 'attribute1' : DataA , ... >

## Minimizing the attribute number:
   1. if there are synonyms, use only one of them consistently.
   2. when modeling binary relations of two principals, use only one of them if not explicitly specified use both.
   For example, when a user is local to a device, the device is also local to the user. Using one "localTo" attribute in one principal is enough to model.

## When building the LHS of each state rule, use minimum related attributes, only those explicitly specified in the premise, and leave others as `...`

## Use special variables "CurrentTime" to express the current time.

## When modeling "compute" something new, fresh key, nonces, and random values: add prefix "Fresh" to the variable name like `FreshKeyA`. 

## Each event should include 3 required fundamental elements: subject, action, object, despite optional arguments.
   Some protocol descriptions do not explicitly specify those 3 elements, but you should figure them out according to the context.
   If, in rare cases, some event really does not need to have an object, use the subject for the object.

## Use the pre-defined function "encrypt" that takes two Qids as inputs and outputs an encrypted Qid. E.g., "encrypt(Qid1,Qid2)"

## "if" grammar should only be used when there is a need to tackle condition that needs do arithmetic comparison.

# The input includes the inital states and a protocol description in natural language.

# The output are state rules in a code block, nothing else, no explanations or comments.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer the below input:
'''

policy_shot_q1 = '''\
[Inital States]
There are 3 principals:
- a device 'deviceB'
- a device 'deviceC'
- a cloud 'cloudA', which records that deviceB's bind key is empty
[State changes]
If any device calls the cloudA's API to record binding keys, the state of the cloudA will update its record for the device's binding key.\
'''

policy_shot_a1 = '''\
```
< cloudA | DeviceX : ('bdKey' : KeyA , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyB
=> < cloudA | DeviceX : ('bdKey' : KeyB , ...) > .
```\
'''

policy_shot_q2 = '''\
[init]
There are 3 principals:
- a user 'userA'
- a user 'userC'
- a device 'deviceB'

[state changes]
When any user is not local to any device and the user approaches the device, the user will be local to the device.
'''
policy_shot_a2 = '''\
< UserX | 'localTo': nils , ... > $ UserX 'approaches' DeviceY
=> < UserX | 'localTo': DeviceY , ... > .
'''


policy_vars_system = f'''\
Imagine you are an engineering expert and you can help me determin variables types of a formalization in a DSL

# The DSL grammar in EBNF
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# Variables use capital strings.

# The input contains a protocol text, the formalization in the DSL, and a list of variables.

# You can determin the type of each variable according the the protocol text and its formalization.

# Possible types
{DSL.Types} 

# The output should strictly be a json file in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''

policy_vars_shot_q1 = '''\
[protocol]
If any device calls the cloudA's API to record binding keys, the cloudA will update its record for that device's binding key.

[formal]
< cloudA | DeviceX : ('bdKey' : KeyA , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyB
=> < cloudA | DeviceX : ('bdKey' : KeyB , ...) > .

[variables] 
["DeviceX", "KeyA", "KeyB", "UserA"]\
'''

policy_vars_shot_a1 = '''\
```
{"DeviceX": "Device", "KeyA":"Qid", "KeyB":"Qid", "UserA":"User"}
```\
'''

event_vars_system = f'''\
Imagine you are an engineering expert and you can help me determin variables types of a formalization in a DSL

# The DSL grammar in EBNF
{DSL.EventRule}
{DSL.Base}

# Variables use capital strings.

# The input contains a protocol text, the formalization in the DSL, and a list of variables.

# You can determin the type of each variable according the the protocol text and its formalization.

# Possible types
{DSL.Types} 

# The output should strictly be a json file in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''

event_vars_shot_q1 = '''\
[protocol]
If any user is local to any device, the user can press the device button.

[formal]
< UserX | 'localTo' : DeviceY , ... > => ev1(UserX, DeviceY) .

[variables] 
["UserX"]\
'''

event_vars_shot_a1 = '''\
```
{"UserX": "User"}
```\
'''

prop_vars_system = f'''\
Imagine you are an engineering expert and you can help me determin variables types of a formalization in a DSL

# The DSL grammar in EBNF
{DSL.Proposition2}
{DSL.Base}

# Variables use capital strings.

# The input contains a protocol text, the formalization in the DSL, and a list of variables.

# You can determin the type of each variable according the the protocol text and its formalization.

# Possible types
{DSL.Types} 

# The output should strictly be a json file in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''

prop_vars_shot_q1 = '''\
[protocol]
ap1 : userC is the owner of deviceB

[formal]
ap1 =| < cloudA | deviceB : ('key' : Qid , 'owner' : userC , ...) > .

[variables] 
["Qid"]\
'''

prop_vars_shot_a1 = '''\
```
{"Qid": "Qid"}
```\
'''

fairness_system = f'''\
Imagine you are a logician, and you can help me formalize behaviors and system properties to LTL formula.

# Use LTL operator symbols below:
<> : Eventually
[] : Always
U : Until
W : Weak until, p W q means that p until q but q does not must to happen
\\/ : Bool logic or
/\\ : Bool logic and
~ : Bool logic not
-> : Logic implication
O : The next time point/The next state

# Use one space between the LTL operators and propositions

# The input will contain atomic propositions and a natural language description of LTL property.

# Only output the LTL formula in a code block, nothing else, no explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now please answer the below input:
'''

fairness_shot_q1 = '''\
[Atomic propositions]
ap1 : The victim performs bind operation 1
ap2 : The victim performs bind operation 2
ap3 : The victim performs bind operation 3 
ap4 : The victim is the device's owner
ap5 : victim takes reset operations
ap6 : attacker performs any operation

[description]
The victim user will always take bind operations in the order until reset (not a must),
and if the victim performs reset, the next state the victim will perform bind operation 1.
In the meantime, the attacker can perform any operations between or after the victim.
It is always the case that if the victim takes reset operation in the next state, the victim takes operation 3 and the victim is not the device owner.  
Eventually, the victim user will be the device owner.\
'''

fairness_shot_a1 = '''\
[](ap1 -> O (ap6 W (ap2 \\/ ap5)))
/\\ [](ap2 -> O (ap6 W (ap3 \\/ ap5)))
/\\ [](ap5 -> O (ap6 W ap1))
/\\ [](O ap5 -> (vop3 /\\ ~ ap4))
/\\ <> ap4\
'''

init_system = '''\
Imagine you are an engineering expert who can help me generate the initial state in a DSL.

# The DSL grammar of the initial state in EBNF is below:
%s
%s

# The input includes a template and a natural language description.

# The template grammar is extended from the DSL, adding choices and type placeholders in attribute values.
%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

# By understanding the natural language description, choose one of choice from choices and replace all the placeholders with constants.

# Modeling negative concept in attribute value:
  If an attribute value has only 2 possibilities, use the boolean value "false" to model the concept of "is not" or "negative." E.g., when a template has "'att1' : [Bool]", use "'att1' : false".
  Else, use "nils" to model the case of "having not" this attribute or the empty set.

# Only output the initial state in a code block, nothing else, no explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer the input below:
''' % (DSL.Init, DSL.Base, DSL.Template, DSL.Types)

init_shot_q1 = '''\
[template]
< userA | ('children' : [User] , 'parents' : {[User] , userB}) > < deviceB | ('online' : [Bool]) > 

[description]
Initially, the userA has no children and the parents are userB; The deviceB is not online.\
'''

init_shot_a1 = '''\
```
< userA | ('children' : nils , 'parents' : userB) > < deviceB | ('online' : false ) >
```\
'''

init_shot_q2 = '''\
[template]
< cloudA | [Device] : ('owner' : [User]) >

[description]
Initially, the cloudA records that deviceB has no owner.\
'''

init_shot_a2 = '''\
```
< cloudA | deviceB : ('owner' : nils) >
```\
'''

rrls_system = '''\
Imagine you are an engineering expert and you can help me generate event rules in a DSL

# The syntax of the DSL is below

%s
%s

# The input contains the state template, event declarations, and natural language description about which user events can happen under which circumstances

# The input state template follows a grammar extended from the DSL, adding choices and type placeholders in attribute values.

%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

# By understanding the natural language description, choose one of choice from choices and replace all the placeholders with constants or variables.

# The output should be thinking process in tag <think></think> and event rules using the grammar <EventRule> in a code block.

# Ensure that the output in code block should not contain any comments.

# The attributes used in output internal states should be from the input state template with the closest meaning

# If the description specifies that a certain action can happen under certain circumstances, only use those circumstances explicitly mentioned, even if other attributes in the state template could hypothetically be relevant.
 If an event does not depend on an attribute from the state template, do not include that attribute as a condition.

# Ensure all the choices/placeholders are replaced by constants or variables in the output. 

i.e., There must not be patterns like `[Device]`, `{[Bool]}`, `{true, false}` in the output.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
''' % (DSL.EventRule, DSL.Base, DSL.Template, DSL.Types)
# Ensure that all the variables appear on the left-hand side first 

rrls_shot_q1 = '''\
[state template]
< userA | ('localTo' : [Device] , 'know' : [Qid]) > < userC | ('localTo' : [Device]) > < deviceB | ('pressed' : [Bool]) >

[events]
eq ev1(UserA, DeviceB) = $ UserA 'approach' DeviceB .
eq ev2(UserA, UserB) = $ UserA 'approach' UserB .
eq ev3(UserA, DeviceB, Key) = $ UserA 'send' DeviceB | Key .

[description]
When any user is not local to any device, the user can approach to any device.
When userA know some key, the user can send the key to deviceB.
'''

rrls_shot_a1Bak = '''\
<think>
Let me break down the task.
# The first sentence.
## The event part is "the user can approach any device", so we find "ev1" in the input events list.
Since the user is "any user" and the device is "any device", which are both retained as variables, I get `ev1(UserA, DeviceB)` on the right-hand side.

## The condition part is "any user is not local to any device", which describes some user's state.
By referring to the input state template, I find two correlated templates "< userA | ('localTo' : [Device] , ...) >" and "< userC | ('localTo' : [Device]) >",
which can be both matched by "< UserA | 'localTo' : [Device] , ... >".
The type placeholder "[Device]" is then instantiated into "nils" in order to express "not local to any device".

## Connect the left-hand side and right-hand side using grammar <EventRule>.

### All the variables ("UserA" and "DeviceB") in RHS must first appear on the LHS.
So add `< DeviceB | ... >` in LHS by refering "< deviceB | ... >" in template.

### Ensure the variables in LHS and RHS are consistent.
Now I get `< UserA | 'localTo' : nils , ... > < DeviceB | ... > => ev1(UserA, DeviceB) .`

# The second sentence.
## The event part is "the user can send the key to deviceB.", so we find "ev3" in the input events list.
Since the user is constant "userA" and device is constant "deviceB", use it to instantiate variable "UserA" and "DeviceB".
Since there is no additional restriction on "key", it is retained as variable "Key". So I get `ev1(userA, deviceB, Key)` on the RHS.

## The condition part is "userA know some key". By referring to input state template, I find "< userA | 'know' : [Qid] , ... >".

### Since the RHS has variable "Key", use it to instantiate the placeholder "[Qid]", I get `< userA | 'know' : Key , ... >` on the LHS.

### Now I am sure all the variables on the RHS first appeared on the LHS.

Now I get `< userA | 'know' : Key , ... > => ev3(userA, deviceB, Key) .`

# Gather together, the answer is:
</think>
```
< UserA | 'localTo' : nils , ... > < DeviceB | ... > => ev1(UserA, DeviceB) .
< userA | 'know' : Key , ... > => ev3(userA, deviceB, Key) .
```
'''

rrls_shot_a1 = '''\
<think>
Let me break down the task.
# The first sentence.
## The event part is "the user can approach any device", so we find "ev1" in the input events list.
Since the user is "any user" and the device is "any device", which are both retained as variables, I get `ev1(UserA, DeviceB)` on the right-hand side.

## The condition part is "any user is not local to any device", which describes some user's state.
By referring to the input state template, I find two correlated templates "< userA | ('localTo' : [Device] , ...) >" and "< userC | ('localTo' : [Device]) >",
which can be both matched by "< UserA | 'localTo' : [Device] , ... >".
The type placeholder "[Device]" is then instantiated into "nils" in order to express "not local to any device".

## Connect the left-hand side and right-hand side using grammar <EventRule>.

### Ensure the variables in LHS and RHS are consistent.
Now I get `< UserA | 'localTo' : nils , ... > < DeviceB | ... > => ev1(UserA, DeviceB) .`

# The second sentence.
## The event part is "the user can send the key to deviceB.", so we find "ev3" in the input events list.
Since the user is constant "userA" and device is constant "deviceB", use it to instantiate variable "UserA" and "DeviceB".
Since there is no additional restriction on "key", it is retained as variable "Key". So I get `ev1(userA, deviceB, Key)` on the RHS.

## The condition part is "userA know some key". By referring to input state template, I find "< userA | 'know' : [Qid] , ... >".

### Since the RHS has variable "Key", use it to instantiate the placeholder "[Qid]", I get `< userA | 'know' : Key , ... >` on the LHS.

Now I get `< userA | 'know' : Key , ... > => ev3(userA, deviceB, Key) .`

# Gather together, the answer is:
</think>
```
< UserA | 'localTo' : nils , ... > < DeviceB | ... > => ev1(UserA, DeviceB) .
< userA | 'know' : Key , ... > => ev3(userA, deviceB, Key) .
```
'''

rrls_shot_q2 = '''\
[state template]
< userA | ('sleepy' : [Bool] , 'own' : [Device]) > < deviceC | ('onoff' : [Bool]) >

[events]
eq ev1(UserA, DeviceB) = $ UserA 'turnOn' DeviceB .
eq ev2(UserA, DeviceB) = $ UserA 'turnOff' DeviceB .

[description]
When any user is not sleepy or not, if the user owns any device, the user can turn the device off.
'''

#covers all the cases of the attribute `sleepy` since the type is `[Bool]`, so it is an independent attribute which should not be included.
rrls_shot_a2 = '''\
<think>
Break down the task.
# The first sentence.
## The event part is "turn the device off", so we find "ev2".
Since the user is "any user" and the device is "any device", which are both retained as variables, I get `ev2(UserA, DeviceB)` on the right-hand side.

## The condition part "When any user is not sleepy or not, if the user owns any device", I have template `< userA | ('sleepy' : [Bool], 'own' : [Device]) >`.
Use variable `DeviceB` to instantiate placeholder `[Device]` and `...` to instantiate `[Bool]` since both sleepy or not are allowed, I get `< UserA | 'sleepy' : ... , 'own' : DeviceB >`.

## Connect the left-hand side and right-hand side using grammar <EventRule>.

### Ensure the variables in LHS and RHS are consistent.
Ok

## Now I get the answer `< UserA | 'sleepy': BoolX , 'own' : DeviceB  > => ev2(UserA, DeviceB) .`
<think>
```
< UserA | 'sleepy': ... , 'own' : DeviceB  > => ev2(UserA, DeviceB) .
```
'''

rrls_shot_a2Bak = '''\
<think>
Break down the task.
# The first sentence.
## The event part is "turn the device off", so we find "ev2".
Since the user is "any user" and the device is "any device", which are both retained as variables, I get `ev2(UserA, DeviceB)` on the right-hand side.

## The condition part "When any user is not sleepy or not, if the user owns any device", I have template `< userA | ('sleepy' : [Bool], 'own' : [Device]) >`.
Use variable `DeviceB` to instantiate placeholder `[Device]` and `...` to instantiate `[Bool]` since both sleepy or not are allowed, I get `< UserA | 'sleepy' : ... , 'own' : DeviceB >`.

## Connect the left-hand side and right-hand side using grammar <EventRule>.

### Ensure all the variables ("UserA" and "DeviceB") in RHS first appear on the LHS.
Ok

### Ensure the variables in LHS and RHS are consistent.
Ok

## Now I get the answer `< UserA | 'sleepy': BoolX , 'own' : DeviceB  > => ev2(UserA, DeviceB) .`
<think>
```
< UserA | 'sleepy': ... , 'own' : DeviceB  > => ev2(UserA, DeviceB) .
```
'''
ap_system = '''\
Imagine you are an engineering expert, and you can help me generate atomic proposition definitions in a DSL.

# the DSL grammar in EBNF

%s
%s

# The input includes the state template, events, and the natural language description of atomic propositions

# The input state template follows a grammar extended from the DSL, adding choices and type placeholders in attribute values.

%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

## By understanding the natural language description, choose one of choice from choices, then replace all the placeholders with constants.

# Use grammar <StateProp> to define those propositions that describing the state, use <EventProp> for those that describing some events happen

# The output should be many proposition definitions with grammar <Proposition> in a code block, not anything else, no explanations

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer: 
''' % (DSL.Proposition, DSL.Base, DSL.Template, DSL.Types)

ap_shot_q1 = '''\
[state template]
< userA | 'age' : [integer] > < serverA | userA : ('guest' : [User], 'foo' : [Qid]) , userC : ('guest' : [User]) > < userC | 'age' : [integer] >

[events]
eq ev1(UserA, UserB, KeyA) = $ UserA 'join' UserB | KeyA .
eq ev2(UserA, UserB, KeyA) = $ UserA 'kick' UserB | KeyA .

[description]
ap1 : userA join userC 's home .
ap2 : serverA records that userC is in the userA 's home.
ap3 : userC takes any operations.  
ap4 : anyone takes operations on userA.\
'''

ap_shot_a1 = '''\
```
ceq E @ S |= ap1 = true if sd(E) == sd(ev1(userA , userC , '')) .
eq E @ S < serverA | userA : ('guest' : userC , ...) , ... > |= ap2 = true .
ceq E @ S |= ap3 = true if subject(E) == userC .
ceq E @ S |= ap4 = true if object(E) == userA .
```\
'''

# performance is worse
ap_systemNew = '''\
Imagine you are an engineering expert, and you can help me formalize atomic proposition definitions in a DSL.

# the DSL grammar in EBNF

%s
%s

# The input includes:1. the state template, 2. events, and 3. description of atomic propositions

## Detailed explanation of part 3
Each of the atomic propositions includes a proposition name on the left of ":", and a natural language meaning on the right.
The proposition name is just a name, you should formalize it according to the meaning.

# The input state template follows a grammar extended from the DSL, adding choices and type placeholders in attribute values.

%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

## By understanding the natural language description, choose one of choice from choices and replace all the placeholders with constants or variables.

# Each proposition definition includes constraints that match the natural description, which can either be internal states or events.

# Determin whether use state constraint or event constraint according to the proposition meaning

# Use internal state constraint to define those propositions that describe the state, use event constraint for those that describe some events that happen

# Constraints of internal states should match the structure of the state template, and can use `...` to match the attribute pairs that are not explicitly specified.

# Ensure all the choices/placeholders from the state template are replaced by constants or variables in the output.

i.e., There must not be patterns like `[Device]`, `{[Bool]}`, `{true, false}` in the output.

# Constraints of events should match the input events, and can use capital-letter variables to match those parts without being explicitly specified.

# The output should be many proposition definitions with grammar <Proposition> in a code block, not anything else, no explanations

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:\
''' % (DSL.Proposition2, DSL.Base, DSL.Template, DSL.Types)
# The output should be many proposition definitions with grammar <Proposition> in a code block, not anything else, no explanations
# The output should be thinking process between tag `<think></think>` and many proposition definitions with grammar <Proposition> in a code block, not anything else, no explanations

ap_shot_q1New = '''\
[state template]
< userA | 'age' : [integer] > < serverA | [User] : ('guest' : [User], 'foo' : [Qid]) > < userC | 'age' : [integer] >

[events]
$ UserA 'join' UserB | KeyA .
$ UserA 'kick' UserB | KeyA .

[description]
ap1 : userA joins userC 's home .
ap2 : serverA records that userC is a guest in userA's home.
ap3 : userC takes any operations.\
'''

ap_shot_a1_cot = '''\
<think>
Let me break down the task.
# ap1
According to the meaning, "userA joins userC 's home" describes an event, so I use an event constraint.
By searching the input event list, I find `$ UserA 'join' UserB | KeyA`.
According to the natural language description, the subject `userA` is clear, so use `userA` to instantiate the variable `UserA`.
The object `userC` is clear, so use `userC` to instantiate `UserB`.
There is no requirement about the argument, so keep the variable `KeyA`.
Finally, I get event constraint `$ userA 'join' userC | KeyA`.

# ap2
"serverA records that userC is in the userA 's home." describes a state of serverA, so I use a state constraint. By searching the input state template, I find `< serverA | [User] : ('guest' : [User], 'foo' : [Qid]) >`.

## Instantiate all the placeholders according to the description.
Use `userA` to instantiate the first `[User]`, and use `userC` to instantiate the second, I get `< serverA | userA : ('guest' : userC ) >`.

## Use `...` to match the rest that are not explicitly specified
`'foo'` is not needed,  use `...` to match.
Finally, I get `< serverA | userA : ('guest' : userC , ...) >`

# ap3
It describes an event, so use an event constraint. It does not explicitly specify what action and what object, the only requirement is that the subject is `userC`.
So use variables `Act` to model any operations, `PrincipalA` to model any object, I get `$ userC Act PrincipalA`.
</think>\
'''

#{ap_shot_a1_cot}
ap_shot_a1New = '''\
```
ap1 =| $ userA 'join' userC | KeyA .
ap2 =| < serverA | userA : ('guest' : userC , ...) > .
ap3 =| $ userC Act PrincipalA .
```\
'''

nap_system = f'''\
Imagine you are a formal logic expert who can help me extract atomic propositions from input text.

# The input includes the natural language description of an LTL property

# Some meaning in the input can be translated to LTL operators (like eventually, always, the next time point/the next state) and Boolean Logic operators (not, and, or), but the others can not, which should be atomic propositions

# Minimize the number of atomic propositions, using short and meaningful names based on their meaning and order. Avoid redundancy or overlapping definitions.

# Define atomic proposition names sequencely like 'ap1', 'ap2', ....

# Define all atomic propositions in affirmative form, even if the input uses a negated description.

# "Some principal do any operations" can be seen as an atomic propositions

# The output should be thinking process in tag <think></think>, and atomic proposition definitions with the name on the left of ":" and the meaning on the right in a code block

# Ensure all atomic propositions must be defined in their affirmative form. Avoid using negations in the definition itself.

## E.g., if the input says "a is not local to b", define the atomic proposition as "alb : a is local to b".

# Ensure there is no LTL operators (including "the next state/the next time point", "eventually", "always") left in the definitions.

## E.g., if the input says "foo in the next state", it becomes "foo".

# Ensure the names in the output are consistant with the input.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''
# In proposition names, there are no underscore characters, use CamelCase instead, lowercase first letter.

nap_shot_q1 = '''\
a is always older than B unless a goes die.
If a dies and b is alive, a will eventually be not older than b in the next state.
Always, a and b eventually die.
If a is not alive, b will be sad the next time.
'''

nap_shot_a1 = '''\
<think>
# First, let me remove LTL context, and separate and extract propositions in the boolean operator "and" and "or", I get
	"a is older than b", "a goes die" from sentence 1; 
	"a dies", "b is alive","a is not older than b" from sentence 2; 
	"a dies","b dies" from sentence 3;
	"a is not alive", "b is sad" from sentence 4.
# Find antonyms: 
## "b is alive" and "b dies". not "be alive" is equal to "dies", 
		choose a better option for simplicity: since "dies" is more, choose it,
		so "b is alive" is replaced by "b dies"
## "a is older than b" and "a is not older than b", for simplicity and the "use affirmative form" principle, choose "a is older than b"
# Find synonyms: 
## "a is not alive" and "a goes die", for simplicity use only "a goes die",
	 Now, "A goes die" and "A dies" are synonyms, use "A dies".
# Let me remove all the "not", only affirmative form left, and remove redundancy, now I have:
	"a is older than b", "a dies", "b dies", "b is sad"
# Give each proposition a short name, now we get:
</think>
```
ap1 : a die
ap2 : b die
ap3 : a is older than b
ap4 : b is sad
```
'''
#ad : a die
#bd : b die
#aob : a is older than b
#bs : b is sad

split_system = '''\
Imagine you are a formal logic expert and you can help me extract and re-oganize information from a protocol description 

# The input contains a protocol description.

# Concept

## The moving agents or actors in a system are "principals", each having its "internal state".

## The changeable properties in internal states are called "attributes".

## The "event" is a relation between the subject principal and object principal, optionally along with some argument data.
   Note that some protocol descriptions do not explicitly specify those 3 elements, but you should figure them out according to the context.
   If, in rare cases, some event really does not need to have an object, use the subject for the object.

# Extract 3 kinds of information from the input:
- How does the system change with some events? It is used to construct state rules in Rewriting Logic.
- How can an event occur under some conditions? It is used to construct event rules in Rewriting Logic.
- The initial states: Including all principals, with their inital attributes value.

# Completeness and accuracy are far more important than simplicity or naturality 

# The output should clearly include the above 3 parts. Each should be concise and in one paragraph, led by a header between brackets like `[Init]`, all in a code block.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''

split_shot_q1 = '''\
Initially, the userC is in the remote and the userA is local to deviceB.
When any user is local to any device, he can leave that device.
Otherwise, he can approach that device.
When any user is remote to any device and the user approaches the device,
the user will be local to the device.\
'''

split_shot_a1 = '''\
```
[Init]
Initially, there are 3 principals:
- a device 'deviceB'
- a user 'userA' who is local to the deviceB
- a user 'userC' who is remote to the deviceB

[State Changes]
When any user is remote to any device and the user approaches the device,
the user will be local to the device.

[Events]
When any user is local to any device, the user can leave that device.
When any user is not local to any device, the user can approach that device.
```\
'''

filter_system = f'''\
Imagine you are an engineering expert and your task is to identify events formalized in a DSL.

# The DSL grammar:
{DSL.Base}
{DSL.Types}


# Principal constants: follows the above grammar, `cloudA` is a constant of type `Cloud`, `userA`, `userB` is constants of type `User`.

# Variables: use capital strings as variables to be as a wildcard in pattern-matching. 
	E.g., `vars DeviceA DeviceB : Device .` defines that `DeviceA` are `DeviceB` are variables of `Device` type to match any device like constant `deviceB` and `deviceC`. 
 
	E.g., `$ DeviceA 'callAPI:setKey' cloudA | KeyB` is an event that models any device can call cloudA's API `'callAPI:setKey'` with any key as an argument.

# The input includes variable definitions, an formalized events list, and a natural language description that express which events occur in which conditions.

# Find the corresponding formalized events whose semantics happen in the description, referring to the variable definitions.

# Events match if their semantics align with the description, exact wording is not required.
	If the events contain variables, refer to variable definitions, all the variable types should match the description.
  
# Carefully ensure all events in the natural language description can find a corresponding event in the input events list.

# Output requirement:
The output should be thinking process in tag <think></think> and a list of numbers in a code block.

# Take your time, think step by step, no hurry to draw a conclusion

Now solve this: 
'''

filter_shot_q1 = '''\
[variables]
vars UserA UserB : User .
vars KeyB : Qid .
vars DeviceX DeviceY : Device .

[events]
$ UserA 'action1' cloudA | KeyB
$ UserB 'action2' DeviceX | KeyB
$ DeviceX 'action1' cloudA | KeyB
$ UserC 'pressButton' DeviceY

[description]
At any time, userC can do action 1 to the cloudA with his key.
If any user is local to any device, any user can: press any device's button; do action 2 with his key on the deviceB.
'''

filter_shot_a1 = '''\
<think>
Let me break down the description. Remove the condition part from the input description, there are 3 events.
1. "userC can do action 1 to the cloudA with his key"
## Parse it into 4 parts:
- Subject: "userC" -> Type: `User`
- Action: "action 1" -> Action: `'action1'`
- Object: "cloudA" 
- Arguments: "with his key" -> Type: `Qid`
### The action part is "action 1", by searching the input events list, I find choices: event 1, and event 3.
### The subject part "userC" is of type "User" and can be matched by variable "UserA" in event 1, but can not be matched by "DeviceX", so exclude event 3.
### The object part "cloudA" is equal to that in event 1
### The arguments part "his key" can be matched by variable "KeyB" (of type "Qid") in event 1
### So event 1 should be in the answer list

2. "any user can press any device's button"
## Parse it...
- Subject: "any user" -> Type: `User` 
- Action: "press the device's button" -> Action: `'pressButton'`
- Object: "any device" -> Type: `Device`
- Argument: None
## Matching events: look for events where a `User` performs `'pressButton'` on a `Device`.
### The most corresponding event is event 4.
- Subject: "UserC" -> Type: `User`
- Object: "DeviceY" -> Type: `Device`
- Argument: None
### All matches, so use event 4.

3. "any user can do action 2 with his key on the deviceB"
## Parse it...
- Subject: "any user" -> Type: `User`
- Action: "action 2" -> Action: `'action2'`
- Object: "the deviceB" ->  Type: `Device`, DeviceX is a variable of type `Device`
- Arguments: "his key" -> Type: `Qid`
## Matching events:  look for events where a `User` performs `'action2'` on a `Device`
### The most corresponding event is event 2.
### Subject "UserB" is of type `User`
### Object "DeviceX" is of type `Device`
### Argument "KeyB" is of type `Qid`
### All matches, use event 2

# Now all the events in description have find the corresponding formalized event.

# Gather together, the answer is:
</think>
```
[1,4,2]
```
'''

#only used in comparison evalutation
genMaudeSystem = '''\
Imagine you are an engineering expert and you can help me generate formalization of the protocol in a Maude

# The grammar

## Strictly follow the following syntax in EBNF
<Maude> ::= sorts <Sort>+ . |
    subsorts <Sort>+ ( < <Sort>+ )+ . |
    op <OpForm> : <Type>* <Arrow> <Type> . |
    ops ( <OpId> | ( <OpForm> ) )+ : <Type>* <Arrow> <Type> . |
    vars <VarId>+ : <Type> . |
    <Statement>|
    <Statement'> .

<Statement>  ::=  eq <Term> = <Term> |
    ceq <Term> = <Term> if <Condition>

<Statement'> ::= rl <Term> => <Term> |
    crl <Term> => <Term> if <Condition'>

<Condition> ::= <ConditionFragment> ( /\\ <ConditionFragment> )*

<Condition'> ::= <ConditionFragment'>
                 ( /\\ <ConditionFragment'> )*

<ConditionFragment> ::= <Term> = <Term> | <Term> := <Term>
                        | <Term> : <Sort>

<ConditionFragment'> ::= <ConditionFragment> | <Term> => <Term>

<Sort> ::= <SortId> | <Sort> { <Sort> ( , <Sort> )* }
<SortId>      %%% simple identifier, by convention capitalized
<VarId>       %%% simple identifier, by convention capitalized
<VarAndSortId> %%% an identifier consisting of a variable name
                   followed by a colon followed by a sort name
<OpId>        %%% identifier possibly with underscores
<OpForm> ::= <OpId> | ( <OpForm> ) | <OpForm>+
<Nat>         %%% a natural number
<Term> ::= <Token> | ( <Term> ) | <Term>+
<Token>       %%% Any symbol other than ( or )
<TokenString> ::= <Token> | ( <TokenString> ) | <TokenString>* 

# The semantics is Rewriting Logic

# The input includes the initial states and a protocol description in natural language.

# The output is Maude code in a code block, nothing else, no explanations or comments.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer the below input:
'''

general_revisor_system = f'''\
Imagine you are an engineering expert, and you can help me revise formalization results according to the requirements below

# The input includes a draft answer and error messages from the feedback of external tools

# Revise the answer according to the error messages

# Note that when the error messages say error at some point, the problem could be at the current and previous positions.

# Minimize modifications

# Output the revised result in a code block

# Take your time, think step by step, no hurry to draw a conclusion
'''

detail_revisor_system = f'''\
Imagine you are an engineering expert, and you can help me revise the above formalization results according to the requirements

# The input includes error messages from the feedback of external tools

# Revise the answer according to the error messages and guide

# Minimize modifications

# Output the full revised result in a code block

# Take your time, think step by step, no hurry to draw a conclusion
'''

# Prepare output for the output function call

policy_revisor_system = f'''\
Imagine you are an engineering expert, and you can help me revise formalization results according to the requirements below

# The revised results should strictly follow the following grammar
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# The input includes a draft answer and error messages from the feedback of external tools

# Revise the answer according to the error messages

# Note that when the error messages say error at some point, the problem could be at the current and previous positions.

# Minimize modifications

# Output the revised result in a code block

# Take your time, think step by step, no hurry to draw a conclusion
'''

#####################################
####Never used in current version####
choose_missing_attributes_system = f'''\
Imagine you are an engineering expert and you can help me revise formalization of the protocol in a DSL

# The DSL grammar
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# The input includes a protocol description, and a list of choices

# The output should a number index in a code block, indicating that which choice should use, e.g. `1` or `2`
'''

choose_missing_attributes_q1 = f'''\
[protocol]
TODO
[choices list]
Choice1:

Choice2:
'''
choose_missing_attributes_a1 = f'''\
```
1
```
'''

nap_revisor_system = f'''\
Imagine you are an engineering expert and you can help me revise specification texts.

# The input includes atomic proposition definitions with the name on the left of ":" and the definitions on the right

# Ensure all atomic propositions must be defined in their affirmative form. Avoid using negations in the definition itself.

# Ensure there is no LTL operators (including "the next state/the next time point", "eventually", "always") in the definitions.

# Ensure there are no Bool Logic operators (including "and", "not", "or") in the definitions, split them into separate atomic propositions.

# The output is just a "OK" without anything else when the protocol is correct, or the full revised proposition definitions in a code block.
'''

nap_revisor_q1 = f'''\
ap1 : userC is not local to deviceB
ap2 : userA is not the owner of deviceC
ap3 : userA takes no operations
'''
nap_revisor_a1 = f'''\
```
ap1 : userC is local to deviceB 
ap2 : userA is the owner of deviceC
ap3 : userA takes operations
```\
'''

nap_revisor_q2 = f'''\
ap1 : userA is local to he deviceB and is the owner of deviceB
'''
nap_revisor_a2 = f'''\
```
ap1 : userA is local to he deviceB
ap2 : userA is the owner of deviceB\
```\
'''

nap_revisor_q3 = f'''\
ap1 : userA presses button
ap2 : userA calls API 'callAPI:setKey'
ap3 : userA calls API 'callAPI:bind'
ap4 : reset happens
ap5 : userA is the owner of deviceB
ap6 : userA performs operations
'''
nap_revisor_a3 = f'''\
OK
'''

revisor_system = f'''\
Imagine you are an engineering expert and you can help me revise formalization of the protocol in a DSL

# The grammar
## Basic syntax in EBNF
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# Check whether the inputs follow this syntax, if not fix the syntax error.

# Additional restrictions that must follow

## If arguments contain one more things, use parenthesis. E.g., In `$ userA 'callAPI' cloudA | (deviceB ; '123')`.

## If events without any argument, do not use `|`

## Ensure all principal's internal states that appear on the LHS of `=` also appear on the RHS, and vice versa.

## Ensure all attributes in every principal's internal state on the LHS also appears in the corresponding internal state on the RHS.
	Otherwise, add the omitted attribute on the RHS with the same value.

## Ensure all attributes in every principal's internal state on the RHS also appear in the corresponding internal state or the event on the LHS . 
	Otherwise, add the omitted attribute on the LHS with value to empty.

## Ensure that all the variables except those that start with the prefix `Fresh` appear on the RHS of `=` must appear in the states or event on the LHS of `=` first.

## Ensure there is a `...` at the end of each set, like `< A | 'att1' : B , ... >`.

## Ensure that all rules have only one event on the LHS of `=`.

## Ensure only one `.` at the end of each rule.

## Ensure there is no comment or explanations in the code block, remove them after identifying.

# Minimizing the attribute number:
  1. if there are synonyms, use only one of them consistently.
   2. when modeling binary relations of two principals, use only one of them if not explicitly specified use both.
   For example, when a user is local to a device, the device is also local to the user. Using one "localTo" attribute in one principal is enough to model.

# The input contains a protocol formalization in the DSL.

# The output is just a "OK" when the protocol is correct, or the thinking process in <think></think> and the revised rules in a code block without comment.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer the below input:
'''

revisor_shot_q1 = '''\
< B | 'att1' : 1 , ... > $ A 'action1' B
=> < B | 'att1' : 2 > .
< A | 'att1' : 1 , ... > $ B 'action2' A
=> < A | 'att1' : 1 , 'att2' : 2 , ... > .
'''

revisor_shot_a1 = '''\
<think>
The first rule has a `...` in B's state on the LHS but does not have it in B's state on the RHS, which is a violation.
So I add a `...` in B's state on the RHS.
The second rule has a mistake, which violates the restriction that all attributes in every principal's internal state on the LHS also appear in the corresponding internal state on the RHS.
So I add a corresponding attribute on the left-hand side and make its value empty.
</think>
```
< B | 'att1' : 1 , ... > $ A 'action1' B
=> < B | 'att1' : 2 , ... > .
< A | 'att1' : 1 , 'att2' : nils , ... > $ B 'action2 ' A 
=> < A | 'att1' : 1 , 'att2' : 2 , ... > .
```
'''

revisor_shot_q2 = '''\
< A | 'att1' : 1, ... > $ A 'action1' B $ B 'action2' A
=>  < A | 'att1' : 2, ... > .
'''

revisor_shot_a2 = '''\
<think>
The first rule has two events, which is a violation.
I separate them into 2 rules that each have only one event.
Since the final result is achieved after both events occur, I created a new attribute 'action1ready' in A's state to synchronize.
</think>
```
< A | 'att1' : 1, 'action1ready' : false , ... > $ A 'action1' B 
=>  < A | 'att1' : 1, 'action1ready' : true , ... > .
< A | 'att1' : 1, 'action1ready' : true , ... > $ B 'action2' A 
=>  < A | 'att1' : 2, 'action1ready' : false , ... > .
```
'''

revisor_shot_q3 = '''\
< B | 'att1' : 1 , ... > $ A 'action1' B
=> < B | 'att1' : 2 , ... > .
'''

revisor_shot_a3 = '''\
OK
'''

revisor_shot_q4 = '''\
< A | 'att1' : 1 , ... > $ B 'action2' A
=> < A | 'att1' : 2 , ... > $ A 'action3' B .
'''

revisor_shot_a4 = '''\
OK
'''

revisor_shot_q5 = '''\
< A | 'att1' : K , 'att1': false , ... >  $ B 'action3' A | K
=> < A | 'att1' : K , 'att2' : true , ... > .
if KeyA == KeyB .
'''

revisor_shot_a5 = '''\
<think>
Detect two `.` in one rule, remove the `.` between `>` and `if`.
</think>
```
< A | 'att1' : K , 'att1': false , ... >  $ B 'action3' A | K
=> < A | 'att1' : K , 'att2' : true , ... > if KeyA == KeyB .
```
'''



#### Deprecated ###
vars_systemBak = f'''\
Imagine you are an engineering expert and you can help me generate variable declarations of a DSL

# The DSL grammar in EBNF
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# Variables use capital strings. E.g., In "$ DeviceX 'callAPI:setKey' cloudA | KeyB", DeviceX is a variable of Device type to match any device.
In contrast, "deviceB" is a constant.

# Variables always begin with a capital letter (e.g., UserX, DeviceY).
  Variables represent dynamic entities that can match multiple instances of their respective type.

# Constants begin with lowercase letters (e.g., cloudA, deviceB).

# Output Requirement: Only declare variables in the output. Do not include constants or their types in the variable declarations.

# Use the grammar below to declare variables:
{DSL.VarDecl}
{DSL.Types} 

# The input contains a protocol formalized in DSL.

# The output should exactly be the variable declarations in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''

vars_shot_q1Bak = '''\
< cloudA | DeviceX : ('bdKey' : KeyA , ...) > $ DeviceX 'callAPI:setKey' cloudA | KeyB
=> < cloudA | DeviceX : ('bdKey' : KeyB , ...) > .
'''
vars_shot_a1Bak = '''\
```
vars DeviceX : Device .
vars KeyA KeyB : Qid .
vars UserA : User .
```
'''
event_system = f'''\
Imagine you are an engineering expert and you can help me identify events in a DSL,

# the DSL grammar in EBNF:
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# The capital strings are for variables to be as a wildcard in pattern-matching. E.g., In $ DeviceX 'callAPI:setKey' cloudA | KeyB , DeviceX is a variable of Device type to match any device. 

# The input inludes a protocol in the DSL state rule and a natural language description about which user events can happen under which circumstances

# Find which events are involved in the input description, and identify the formalized of them from the DSL protocol.

# If there are equal events, remove the replication.

# The output should be event declarations in a code block, nothing else, no explanations.

# Event declaration grammar:
{DSL.EventDecl}

Now, please answer the below input:
'''

event_shot_q1 = '''\
[protocol]
< cloudA | 'att1' : KeyA ) > $ UserA 'action1' cloudA | KeyB
=> < cloudA | 'att1' : KeyB ) > .
< DeviceX |  'att1' : KeyA , ... > < UserA | 'localTo' : DeviceX , ... > $ UserA 'action2' DeviceX | KeyB
=> < DeviceX |  'att1' : KeyB , ... > < UserA | 'localTo' : DeviceX , ... > $ DeviceX 'action3' cloudA | KeyB .

[description]
In any time, userC can do action 1 to the cloudA with his key.
When the userC is not local to the any device, he can do action 2 to the deviceB.
'''

event_shot_a1 = '''\
```
eq ev1(UserA,KeyB) = $ UserA 'action1' cloudA | KeyB .
eq ev2(UserA, DeviceX, KeyB) = UserA 'action2' DeviceX | KeyB .
```
'''


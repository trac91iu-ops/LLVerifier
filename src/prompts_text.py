#!/bin/python3
# TODO add constant parsing, and constant definition
import DSLPrompt as DSL

policy_system = f'''\
Generate state rules in the existing DSL from the supplied initial state and protocol description.

# Grammar
{DSL.StateRule}
{DSL.Base}
{DSL.Condition}

# Source fidelity
Use only the supplied description, not a reference/gold model or assumed security policy.
Preserve every explicit guard, state update, message direction, action name, and argument
(including device identifiers, keys, context identifiers, payloads, and returned histories).
Keep argument order and arity consistent across every occurrence of an event. Multiple
arguments use a parenthesized semicolon list; omit `|` only for zero arguments.
Map diagram aliases consistently. Generic roles such as any user are typed capitalized
variables; explicitly named actors remain constants. Do not specialize a generic role to
an owner or merge two distinct roles just because they can denote the same principal.
Use only library principal constants: userA through userD, deviceA through deviceD,
cloudA through cloudD, clientA through clientD, serverA through serverD, appA through
appD, deviceLock, deviceSwitch, cloudGoogle, cloudSmartThing, cloudIFTTT.
Other data names are quoted Qids, not new principal constants. Keep given library names.

# State and conditions
Represent explicitly described mutable values and guard facts as attributes. Retain initial
facts and explicit conditions even if they do not change in this rule. Do not invent schema
keys for ownership, authorization, acknowledgement, progress, phases, or scheduling.
Use consistent attribute names; preserve distinct stores (e.g. a user's key and a cloud's
record for that user). Do not merge distinct relationships to minimize the schema.
Use only the attributes needed for the stated guard or update, with `...` for the rest.
Keep each matched principal and attribute on both sides; unchanged values stay unchanged.
For an overwritten value, match a variable on the LHS unless the source explicitly requires
an empty or particular old value. Never invent an empty-value precondition.
Express equality, membership and conjunctions of state facts by shared variables and LHS
patterns. Use `if` for a supported comparison, including explicit inequality; the grammar
supports one comparison, not arbitrary Boolean expressions. Express alternative cases as
separate rules. Do not silently drop a condition or encode unsupported syntax or a made-up
Boolean attribute to conceal a condition the grammar cannot express.
`nils` denotes an empty value/set, `false` a false Boolean. Use comma-separated sets for
unordered membership/history and semicolon-separated lists for ordered event arguments.
Use variables for arbitrary old values and `Fresh`-prefixed variables only for explicitly
fresh generated data. Other RHS variables must be bound by LHS state or event patterns;
`CurrentTime` is the special current-time variable. Use only supported functions such as
`encrypt(Qid1,Qid2)`, never invent helper functions.
The DSL does not accept lowercase `system`, `randomStr(...)`, or arithmetic expressions
as attribute values on the RHS. Lower explicit fresh/random generation to a `Fresh`-prefixed
Qid variable (e.g. FreshKeyA), so the existing transformer introduces its counter and
random-value machinery. Use `CurrentTime` for current-time values/comparisons so the
transformer introduces time state. Do not delete freshness/time semantics, substitute a
fixed secret, invent a principal for system, or manually emit counter arithmetic. Runtime
counter/time bookkeeping is transformer-owned rather than a DSL principal to initialize.
Ordered lists are not sets: preserve ordered event arguments with semicolons. Do not emit
`list(L)` unless the supplied grammar supports it; do not silently replace ordered-list
semantics by unordered sets.
A snoop/discovery action that changes knowledge needs an event-driven state handler that
updates the knowledge attribute. Its event-availability rule only enables the event and
cannot mutate state. Preserve explicit authentication and context-existence guards without
adding ownership checks.
The DSL has no `owise` or branch priority. Encode response alternatives with disjoint LHS
guards, e.g. an initial response for knowCtx=nils and receivedHistory=nils versus a
continuation for knowCtx=Ctx where Ctx has type Qid (which excludes nils). Do not emit an
unconstrained fallback overlapping the initial handler; cover other explicitly stated
cases using their own disjoint patterns.

# Actions and processing
Independent optional blocks describe independently enabled actions, not a total schedule,
mandatory execution, or fairness. Do not add ordering or progress state from their order.
Distinguish outer action-availability guards from inner processing/effect guards. Outer
availability guards (the condition of the outermost block) are formalized later as separate
event rules; keep them out of state rules, and do not turn an inner success test into an
availability restriction. No owner, authentication, key, proximity, or acknowledgement check is implied
by an action name. In particular, do not repair an explicitly missing security check.
An event-driven state rule has one incoming event on the LHS and at most one outgoing
event on the RHS. Replies/forwarding are generated by the triggering rule and consumed by
subsequent rules, with their actual senders, receivers and complete arguments. They are not
independently initiated merely because they appear as arrows. Retain upstream updates when
a downstream event has no matching processing rule.
Automatic state changes with no triggering message use event-free state rules, as allowed
by LogicalState. Do not invent a user event. Match an explicit old state/guard so the rule
ceases to apply after its update; never emit an identical-state or endlessly reapplicable
automatic equation. Do not impose priority on overlapping behaviors unless stated.
For no-op attempts, do not invent error replies or state changes. The pipeline extracts its
event inventory from these rules: preserve an otherwise unrepresented independent no-op
event with a consuming rule, e.g. `< DeviceX | ... > $ UserX 'attempt' DeviceX
=> < DeviceX | ... > .` The event disappears, so this is not a self-loop equation.
If an event already occurs in another rule, unmatched attempts can use the runtime's
normal event discard behavior. Never retain the same incoming event on an unchanged RHS.

# Output
Return only DSL state rules in one code block, with a single final `.` per rule.
No Maude modules, declarations, prose, comments, properties, or new syntax.
'''





# Type list with the meaning of each type, shared by the three variable-type prompts
# (policy, event and proposition variables); definitions follow lib/aux.maude and lib/Iot.maude.
_varTypes = f'''\
# Possible types
{DSL.Types}

# Meaning of each type
- Qid: a quoted constant, e.g. 'secretA' or 'near'. A key, token, password or secret that must be present is a Qid.
- Nat / Bool: a natural number / true or false.
- User, Device, Cloud, App, Server, Client: one principal of that kind, e.g. userA, deviceB, cloudA.
- Principal: a principal of any kind.
- Item: any single value: a principal, a Qid, a Nat, a Bool, or a pair `a : b`.
- Key: the name on the left of a pair `a : b`, such as the attribute name 'near', or deviceB in
  `deviceB : (...)`. It is not a cryptographic key.
- Set: zero or more items joined by `,`; `nils` is the empty set. Only Set matches `nils`, so a variable
  whose value may be absent when the rule fires must be Set, e.g. an old value that is replaced whatever it
  was, or a key the user may not have yet.
- List: ordered items joined by `;`.
- Action: the action name of an event. Arguments: the arguments of an event.
  Attributes: all attributes of a principal.\
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

{_varTypes}

# Every sort except Set excludes the empty value `nils`: a variable of sort Item, Principal, User, Device,
Qid, Key, Bool, ... never matches `nils`. Choose Set when the variable must also match an empty value,
e.g. an old value that is overwritten whatever it was, including none. Choose a specific sort when the
source requires a non-empty value, e.g. 'holds a key' or 'is associated with a device'.

# The output should strictly be a json file in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''



event_vars_system = f'''\
Imagine you are an engineering expert and you can help me determin variables types of a formalization in a DSL

# The DSL grammar in EBNF
{DSL.EventRule}
{DSL.Base}

# Variables use capital strings.

# The input contains a protocol text, the formalization in the DSL, and a list of variables.

# You can determin the type of each variable according the the protocol text and its formalization.

{_varTypes}

# Every sort except Set excludes the empty value `nils`: a variable of sort Item, Principal, User, Device,
Qid, Key, Bool, ... never matches `nils`. Choose Set when the variable must also match an empty value,
e.g. an old value that is overwritten whatever it was, including none. Choose a specific sort when the
source requires a non-empty value, e.g. 'holds a key' or 'is associated with a device'.

# The output should strictly be a json file in a code block, not anything else, without explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
'''



prop_vars_system = f'''\
Imagine you are an engineering expert and you can help me determin variables types of a formalization in a DSL

# The DSL grammar in EBNF
{DSL.Proposition2}
{DSL.Base}

# Variables use capital strings.

# The input contains a protocol text, the formalization in the DSL, and a list of variables.

# You can determin the type of each variable according the the protocol text and its formalization.

{_varTypes}

# Every sort except Set excludes the empty value `nils`: a variable of sort Item, Principal, User, Device,
Qid, Key, Bool, ... never matches `nils`. Choose Set when the variable must also match an empty value,
e.g. an old value that is overwritten whatever it was, including none. Choose a specific sort when the
source requires a non-empty value, e.g. 'holds a key' or 'is associated with a device'.

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

# The input includes a template, a threat model and a natural language description.
The threat model states the roles and the situation before the attack starts; it holds
unless the description states otherwise. Map its facts onto the template attributes that
express them, e.g. "near the device" onto a proximity attribute; skip a fact that no
attribute expresses.

# The template grammar is extended from the DSL, adding choices and type placeholders in attribute values.
%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

# Explicit initial values in the description take precedence over inferred template
choices, including when a template only shows a value reached later. Preserve every
explicit initial fact, nested record and principal; do not initialize to a later state.
Use the template as a schema aid, not evidence that a credential or owner initially exists.
Keep explicit false and nils values. Anything that neither the description nor the threat
model states is absent initially: use a type-compatible empty value (nils, or false as
described below), never invent a nonempty credential, owner, permission or principal.
So the description need not say that something is empty, off, unpressed or unrecorded.
Replace placeholders with ground values; do not output variables, choices or ellipses.
Never omit a template attribute: an absent value is written as nils or false. Template
records under the same placeholder key, e.g. two `[User] : (...)` records, are views of
one kind of record taken from different rules; give every concrete record of that kind
all attributes of those views. A principal without attributes is written `< p | nils >`.
Use only library principal constants: userA through userD, deviceA through deviceD,
cloudA through cloudD, clientA through clientD, serverA through serverD, appA through
appD, deviceLock, deviceSwitch, cloudGoogle, cloudSmartThing, cloudIFTTT.
Map aliases consistently with the description/template; other data names are quoted Qids.
The DSL cannot name lowercase system. Counter/time bookkeeping for Fresh-prefixed values
and CurrentTime is inserted by the transformer; do not invent a system principal or
manually encode arithmetic initial values. Preserve all ordinary explicit initial facts.
Do not invent principal constants to fill a placeholder or add unrelated principals.

# Modeling negative concept in attribute value:
  If an attribute value has only 2 possibilities, use the boolean value "false" to model the concept of "is not" or "negative." E.g., when a template has "'att1' : [Bool]", use "'att1' : false".
  Else, use "nils" to model the case of "having not" this attribute or the empty set.

# Only output the initial state in a code block, nothing else, no explanations.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer the input below:
''' % (DSL.Init, DSL.Base, DSL.Template, DSL.Types)





rrls_system = '''\
Imagine you are an engineering expert and you can help me generate event rules in a DSL

# The syntax of the DSL is below

%s
%s

# The input contains the state template, event declarations, and natural language description about which independent events can happen under which circumstances

# The input state template follows a grammar extended from the DSL, adding choices and type placeholders in attribute values.

%s
%s

## [A] means a placeholder of type A. E.g., `[Bool]` can be replaced by constants `true` or `false`.

## {[A], [B], c} means choices where there are 3 possible replacements: a constant of type `A`, a constant of type `B`, and a constant `c`.

E.g., the placeholder "{[Bool], 'foo'}" can either be replaced by `true`, `false`, `'foo'`.

# By understanding the natural language description, choose one of choice from choices and replace all the placeholders with constants or variables.

# Generate only independently initiable action rules, including explicitly independent
cloud/device/self actions. Replies and forwarding are internal responses, not choices.
Cover all supplied event forms described as independently enabled, including no-op attempts.
Preserve exactly the supplied evN identifier and its parameter order/arity; instantiate
arguments without renaming or renumbering declarations. Never use an identifier from a
different template merely because the action names resemble one another.
Use actual outer availability guards, not inner processing/success tests. Do not add
ownership, permissions, acknowledgement, or sequencing requirements. Independent optional
blocks are not a total schedule. Preserve generic roles as variables and named actors as
constants. Match argument values to the stated state source (including nested records).
Every variable in the generated event must be bound by a left-hand state pattern.
A type declaration alone does not bind a value. Fresh-prefixed variables and CurrentTime
are not exceptions for event rules. Use source-supported constants for literal arguments;
do not invent knowledge attributes or availability guards to bind an unspecified argument.
Conjoin guard facts with LHS patterns and shared variables; alternatives need separate
rules. Use only conditions expressible by EventRule: it has no `if` clause. Do not drop
unrepresentable guards or invent new schema keys to pretend to encode them.
Use `< PrincipalX | ... >` for an explicit existence guard. Omit unrelated attributes;
`...` belongs at the end of an attribute set, not as an attribute value.

# `nils` is the empty value. It fits every attribute placeholder, whatever its type, and expresses absence such as 'not near any device' or 'holds no key' (e.g. `'near' : nils`).
# Sets are unordered and `nils` is their identity, so membership is a pattern: `'members' : (UserY , Rest)` matches any set that contains UserY (Rest may be empty).
# Each principal occurs once in the state, so separate patterns in one rule match different principals: `< UserX | ... > < UserY | ... >` already means two distinct users. A guard such as 'distinct users UserX and UserY' needs nothing more.
# Output only event rules in one code block, without explanation or thinking tags.

# Ensure that the output in code block should not contain any comments.

# Reuse the exact matching attributes from the input template; do not substitute a merely similar fact or invent schema keys.

# If the description specifies that a certain action can happen under certain circumstances, only use those circumstances explicitly mentioned, even if other attributes in the state template could hypothetically be relevant.
 If an event does not depend on an attribute from the state template, do not include that attribute as a condition.

# Ensure all the choices/placeholders are replaced by constants or variables in the output. 

i.e., There must not be patterns like `[Device]`, `{[Bool]}`, `{true, false}` in the output.

# Take your time, think step by step, no hurry to draw a conclusion

Now, please answer:
''' % (DSL.EventRule, DSL.Base, DSL.Template, DSL.Types)
# Ensure that all the variables appear on the left-hand side first 


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
Since there is no additional restriction on "key", it is retained as variable "Key". So I get `ev3(userA, deviceB, Key)` on the RHS.

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



#covers all the cases of the attribute `sleepy` since the type is `[Bool]`, so it is an independent attribute which should not be included.

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

filter_system = f'''\
Select independently initiable events from the supplied DSL event inventory.
{DSL.Base}
{DSL.Types}
The inventory is ordered: an unlabeled line has its original 1-based position. Return
those positions, never renumber after filtering or synthesize missing entries. If explicit
numeric labels are supplied, retain those labels. Preserve input order in the result.
Match subject type and identity, action, receiver/direction, argument count, argument order
and constants, not just the action name. A generic typed variable can match a stated
specific actor; a fixed actor must not stand in for every actor. Cover every matching
independent event form, including forms differing in payload, receiver, or arity.
Use the description's actual availability guards to identify independent actions. Do not
exclude an attempted action because its processing/success guard may fail. Include stated
independent cloud/device/self actions as well as user actions. Exclude internal replies,
acknowledgements and forwarding unless explicitly independently enabled. Do not impose a
schedule, ownership check, or other extra condition. State-only automatic changes are not
events. Do not invent an event or index when a described form is missing from the inventory.
Output only a list of unique integer positions in one code block (e.g. [1, 3]); use []
when none match. No explanation or thinking tags.
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

# The input inludes a protocol in the DSL state rule and a natural language description about which independent events can happen under which circumstances

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
eq ev2(UserA, DeviceX, KeyB) = $ UserA 'action2' DeviceX | KeyB .
```
'''



# Appended to the diagram for genPolicy/genRRLs when the input is split into blocks (see diagram.py).
block_label_instruction = '''\
[Output labels]
Each top-level block of the diagram above is tagged with a label such as `[B1]`; a message
outside any block carries its label right after the colon. Prefix every rule you output with
the label of the block it formalizes:
[B1] <rule> .
[B1] <another rule from the same block> .
[B2] <rule> .
Exactly one rule follows each label; repeat the label for further rules from the same block.
A rule that handles a reply or forwarded message belongs to the block in which that message is sent.
The labels are the only additions; the rules themselves keep the required DSL syntax.
'''


# ---- Diagram few-shot examples ----
# Two small vendor-neutral protocols drawn like sequence_diagram/input/*/diagram.md. Every
# rule-generation agent takes its examples from them, and each question is built exactly like
# the real input (labeled with diagram.annotate). Naming convention shown to the model:
# `actor UserX` stays a variable; `participant Device` -> deviceB, `participant Cloud` -> cloudA.
from diagram import splitDiagram as _split, annotate as _annotate
from threat_models import threatModel

def _labeled(d):
    return _annotate(d, _split(d))

fewshot_diagram1 = '''\
```mermaid
sequenceDiagram
    actor UserX
    participant Device
    participant Cloud
    Note over UserX,Cloud: Initially every user is away from the device and holds its own token.
    alt The user is away from the device
        UserX->>Device: The user walks up to the device
        Note over UserX: The user is now next to the device.
    end
    alt The user is next to the device and holds a token
        UserX->>Device: The user submits the token to the device
        opt The device is unlocked
            Note over Device: The device stores the token, replacing any stored token, and locks itself.
            Device->>Cloud: The device uploads the token to the cloud
            Note over Cloud: The cloud records the token for the device, replacing any earlier record.
        end
    end
    alt The user holds a token
        UserX->>Cloud: The user asks the cloud to revoke the device's token, presenting the token
        opt The presented token matches the cloud record for the device
            Note over Cloud: The cloud clears its token record for the device.
            Cloud-->>UserX: The cloud confirms the revocation to the user
            Note over UserX: The user discards its token.
        end
    end
```
'''

fewshot_diagram2 = '''\
```mermaid
sequenceDiagram
    actor UserX
    participant Device
    alt The user is next to the device
        UserX->>Device: The user walks away from the device
        Note over UserX: The user is now away from the device.
    end
    UserX->>Device: The user pings the device
    alt The user is next to the device
        UserX->>Device: The user presses the reset button of the device
        opt The device is busy
            Note over Device: The device becomes idle and drops its current job.
        end
    end
    alt The device is idle and holds a job
        Note over Device: The device starts the job and becomes busy.
    end
```
'''

# State rules: only Notes become updates; outer guards are left to event rules; replies and
# forwarded messages are emitted on the RHS and consumed by their own rule; an ignored branch
# yields no rule; an action with no state effect keeps a consuming rule; an automatic block
# changes state so that it stops applying.
_policy1 = '''\
< UserX | 'near' : nils , ... > $ UserX 'walkUp' deviceB
=> < UserX | 'near' : deviceB , ... > .
< deviceB | 'locked' : false , 'token' : OldToken , ... > $ UserX 'submitToken' deviceB | (Token)
=> < deviceB | 'locked' : true , 'token' : Token , ... > $ deviceB 'uploadToken' cloudA | (Token) .
< cloudA | deviceB : ('token' : OldToken , ...) > $ deviceB 'uploadToken' cloudA | (Token)
=> < cloudA | deviceB : ('token' : Token , ...) > .
< cloudA | deviceB : ('token' : Token , ...) > $ UserX 'revokeToken' cloudA | (deviceB ; Token)
=> < cloudA | deviceB : ('token' : nils , ...) > $ cloudA 'confirmRevoke' UserX | (deviceB) .
< UserX | 'token' : Token , ... > $ cloudA 'confirmRevoke' UserX | (deviceB)
=> < UserX | 'token' : nils , ... > .'''
_policy1Labels = ['B1', 'B2', 'B2', 'B3', 'B3']
_policy2 = '''\
< UserX | 'near' : deviceB , ... > $ UserX 'walkAway' deviceB
=> < UserX | 'near' : nils , ... > .
< deviceB | ... > $ UserX 'ping' deviceB
=> < deviceB | ... > .
< deviceB | 'busy' : true , 'job' : Job , ... > $ UserX 'pressReset' deviceB
=> < deviceB | 'busy' : false , 'job' : nils , ... > .
< deviceB | 'busy' : false , 'job' : Job , ... >
=> < deviceB | 'busy' : true , 'job' : Job , ... > .'''
_policy2Labels = ['B1', 'B2', 'B3', 'B4']

# Event rules: one per initiated message, guarded by its outer block condition only
# (including absence such as 'near' : nils); every event argument is bound on the LHS.
_rrls1 = '''\
< UserX | 'near' : nils , ... > => ev1(UserX) .
< UserX | 'near' : deviceB , 'token' : Token , ... > => ev2(UserX, Token) .
< UserX | 'token' : Token , ... > => ev3(UserX, Token) .'''
_rrls1Labels = ['B1', 'B2', 'B3']
_rrls2 = '''\
< UserX | 'near' : deviceB , ... > => ev1(UserX) .
< UserX | ... > < deviceB | ... > => ev2(UserX) .
< UserX | 'near' : deviceB , ... > => ev3(UserX) .'''
_rrls2Labels = ['B1', 'B2', 'B3']

def _withLabels(rules, labels):
    chunks = [c for c in (rules + '\n').split(' .\n') if c.strip()]
    assert len(chunks) == len(labels), 'one block label per few-shot rule'
    return '\n'.join(f'[{l}] {c} .' for l, c in zip(labels, chunks))

_template1 = "< userA | ('token' : [Qid] , 'near' : [Principal]) > < userC | ('token' : [Qid] , 'near' : [Principal]) > < deviceB | ('token' : [Set] , 'locked' : [Bool]) > < cloudA | ([Principal] : ('token' : {[Qid] , [Set]})) >"
_template2 = "< userA | ('near' : [Principal]) > < userC | ('near' : [Principal]) > < deviceB | ('busy' : [Bool] , 'job' : [Qid]) >"
_events1 = '''\
$ UserX 'walkUp' deviceB
$ UserX 'submitToken' deviceB | (Token)
$ deviceB 'uploadToken' cloudA | (Token)
$ UserX 'revokeToken' cloudA | (deviceB ; Token)
$ cloudA 'confirmRevoke' UserX | (deviceB)'''
_eventDecls1 = '''\
eq ev1(UserX) = $ UserX 'walkUp' deviceB .
eq ev2(UserX, Token) = $ UserX 'submitToken' deviceB | (Token) .
eq ev3(UserX, Token) = $ UserX 'revokeToken' cloudA | (deviceB ; Token) .'''
_eventDecls2 = '''\
eq ev1(UserX) = $ UserX 'walkAway' deviceB .
eq ev2(UserX) = $ UserX 'ping' deviceB .
eq ev3(UserX) = $ UserX 'pressReset' deviceB .'''

_fence = lambda s: '```\n' + s + '\n```'
_ruleDesc = lambda d: _labeled(d) + '\n\n' + block_label_instruction

policy_shot_q1 = _ruleDesc(fewshot_diagram1)
policy_shot_a1 = _fence(_withLabels(_policy1, _policy1Labels))
policy_shot_q2 = _ruleDesc(fewshot_diagram2)
policy_shot_a2 = _fence(_withLabels(_policy2, _policy2Labels))

policy_vars_shot_q1 = f'''\
[protocol]
{_labeled(fewshot_diagram1)}

[formal]
{_policy1}

[variables]
['OldToken', 'Token', 'UserX']'''
policy_vars_shot_a1 = _fence('{"OldToken": "Set", "Token": "Qid", "UserX": "User"}')

event_vars_shot_q1 = f'''\
[protocol]
{_labeled(fewshot_diagram1)}

[formal]
{_rrls1}

[variables]
['Token', 'UserX']'''
event_vars_shot_a1 = _fence('{"Token": "Qid", "UserX": "User"}')

# The forwarded upload (3) and the reply (5) are internal, not independently initiated.
filter_shot_q1 = f'''\
[events]
{_events1}

[description]
{_labeled(fewshot_diagram1)}'''
filter_shot_a1 = _fence('[1, 2, 4]')

# Initial facts: the diagram overrides the threat model (shot 1: users start away and hold tokens);
# the threat model places the owner near the device (shot 2); anything else is empty.
init_shot_q1 = f'''\
[template]
{_template1}

[threat model]
{threatModel()}

[description]
{_labeled(fewshot_diagram1)}'''
init_shot_a1 = _fence("< userA | ('near' : nils , 'token' : 'tokenA') > < userC | ('near' : nils , 'token' : 'tokenC') > < deviceB | ('locked' : false , 'token' : nils) > < cloudA | (deviceB : ('token' : nils)) >")
init_shot_q2 = f'''\
[template]
{_template2}

[threat model]
{threatModel()}

[description]
{_labeled(fewshot_diagram2)}'''
init_shot_a2 = _fence("< userA | ('near' : deviceB) > < userC | ('near' : nils) > < deviceB | ('busy' : false , 'job' : nils) >")

rrls_shot_q1 = f'''\
[state template]
{_template1}

[events]
{_eventDecls1}

[description]
{_ruleDesc(fewshot_diagram1)}'''
rrls_shot_a1 = _fence(_withLabels(_rrls1, _rrls1Labels))
rrls_shot_q2 = f'''\
[state template]
{_template2}

[events]
{_eventDecls2}

[description]
{_ruleDesc(fewshot_diagram2)}'''
rrls_shot_a2 = _fence(_withLabels(_rrls2, _rrls2Labels))

# ---- Property-template slots (check mode) ----
slots_system = f'''\
Instantiate the state propositions of a predefined security property for a protocol model in a DSL.

# Grammar
{DSL.Proposition2}
{DSL.Base}

# The input has the state template of the model, its initial state, its state rules, the roles,
# and the slots: each slot is a name and the fact it must express.
# For every slot output exactly one proposition `name =| <InternalState> .` that holds exactly when
# the fact holds. A slot is a state fact: never use an event.
# Use only principals, attributes and record nesting that occur in the template, the initial state
# and the rules; use the role constants given in [roles]; end every attribute set with `...`.
# Pick the attribute whose value the rules update for that fact (e.g. the owner record that a bind
# rule writes), not a similar-looking one.
# `nils` is the empty value. Sets are unordered with identity `nils`, so membership is a pattern:
# `'owner' : (userC , Rest)` holds whenever userC is among the owners (Rest may be empty).
# A principal key takes a parenthesized value: `deviceB : ('owner' : (userC , Rest) , ...)`.
# Output only the propositions in one code block, one per line, no explanation.
'''

slots_shot_q1 = '''\
[state template]
< userA | ('token' : [Qid] , 'near' : [Principal]) > < userC | ('token' : [Qid] , 'near' : [Principal]) > < deviceB | ('token' : [Set] , 'locked' : [Bool]) > < cloudA | ([Principal] : ('token' : {[Qid] , [Set]} , 'holders' : [Set])) >

[initial state]
< userA | ('near' : deviceB , 'token' : 'tokenA') > < userC | ('near' : nils , 'token' : 'tokenC') > < deviceB | ('locked' : false , 'token' : nils) > < cloudA | (deviceB : ('token' : nils , 'holders' : nils)) >

[state rules]
eq < cloudA | (deviceB : ('token' : Token , 'holders' : Holders , ..) , ...) > $ UserX 'claim' cloudA | (deviceB ; Token)
= < cloudA | (deviceB : ('token' : Token , 'holders' : (Holders , UserX) , ..) , ...) > .
eq < UserX | ('near' : OldNear , ..) > $ UserX 'walkUp' deviceB
= < UserX | ('near' : deviceB , ..) > .

[roles]
attacker: userC
victim: userA
device: deviceB
cloud: cloudA

[slots]
attackerLocal : the attacker is near / local to the device
attackerOwner : the attacker is recorded as an owner of the device'''

slots_shot_a1 = '''\
```
attackerLocal =| < userC | 'near' : deviceB , ... > .
attackerOwner =| < cloudA | deviceB : ('holders' : (userC , Rest) , ...) , ... > .
```'''

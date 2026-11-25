# Kevo: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## b7385b65d578.json (run2)

effect acc 66.7 rec 66.7; exact acc 33.3 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendMessage' UserX | (encrypt(randomStr('R', N), Key)) .`
- r4: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendMessage' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r6: `eq < cloudA | (deviceB : ('owners' : (UserX , Owners) , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : (nils , Owners) , ..) , ...) > .`

## 1e503478afb7.json (run3)

effect acc 57.1 rec 66.7; exact acc 28.6 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'deliverMessage' UserX | (encrypt(randomStr('R', N), Key)) .`
- r4: `eq < UserX | ('message' : nils , ..) > $ deviceB 'deliverMessage' UserX | (M) = < UserX | ('message' : M , ..) > .`
- r5: `ceq < UserX | ('message' : StoredMessage , ..) > $ deviceB 'deliverMessage' UserX | (M) = < UserX | ('message' : StoredMessage , ..) > if StoredMessage =/= nils .`
- r6: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : ('owner' : UserX , Owners) , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : ('owner' : UserX , Owners) , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : ('owner' : nils , Owners) , ..) , ...) > .`

## d169b6b5c01a.json (a2-run3)

effect acc 66.7 rec 66.7; exact acc 33.3 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendMessage' UserX | (encrypt(randomStr('R', N), Key)) .`
- r4: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendMessage' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r6: `eq < cloudA | (deviceB : ('owners' : (UserX , OtherOwners) , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : (nils , OtherOwners) , ..) , ...) > .`

## 58a85c856834.json (run5)

effect acc 57.1 rec 66.7; exact acc 28.6 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendMessage' UserX | (encrypt(randomStr('R', N), Key)) .`
- r4: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendMessage' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r5: `ceq < UserX | ('message' : StoredMessage , ..) > $ deviceB 'sendMessage' UserX | (Message) = < UserX | ('message' : StoredMessage , ..) > if StoredMessage =/= nils .`
- r6: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : ('owner' : UserX , Owners) , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : ('owner' : UserX , Owners) , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : ('owner' : nils , Owners) , ..) , ...) > .`

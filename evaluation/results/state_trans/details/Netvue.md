# Netvue: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 96853ab6bbe3.json (run1, run2, run3, run5)

effect acc 66.7 rec 66.7; exact acc 33.3 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |
| r2 |  |  |  | exact |  |  |
| r3 |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 | exact (gen wider) |  |  |  |  |  |
| r6 |  | exact (gen wider) |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendEncryptedText' UserX | (encrypt(randomStr('R', N), Key)) .`
- r2: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendEncryptedText' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (deviceB : ('owners' : (UserX , Owners) , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : (nils , Owners) , ..) , ...) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 6d19a49bff8b.json (run4)

effect acc 66.7 rec 66.7; exact acc 33.3 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |
| r2 |  |  |  | exact |  |  |
| r3 |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 | exact (gen wider) |  |  |  |  |  |
| r6 |  | exact (gen wider) |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendEncryptedText' UserX | (encrypt(randomStr('R', N), Key)) .`
- r2: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendEncryptedText' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (deviceB : ('owners' : (UserX , OtherOwners) , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB) = < cloudA | (deviceB : ('owners' : (nils , OtherOwners) , ..) , ...) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 257afe73cfca.json (run4)

effect acc 66.7 rec 66.7; exact acc 33.3 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |
| r2 |  |  |  | exact |  |  |
| r3 |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 | exact (gen wider) |  |  |  |  |  |
| r6 |  | exact (gen wider) |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : KeyA , ...) > $ DeviceY 'send' UserX | (encrypt(randomStr('RandomString', N), KeyA)) .`
- g4: `eq < UserX | ('message' : nils , ..) > $ DeviceY 'send' UserX | (MessageA) = < UserX | ('message' : MessageA , ..) > .`
- g5: `eq < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (encrypt(FreshRandomString, KeyA)) = < system | ('counter' : N , ..) > < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ...) , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : Key , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : Key , ...) > $ deviceB 'sendEncryptedText' UserX | (encrypt(randomStr('R', N), Key)) .`
- r2: `eq < UserX | ('message' : nils , ..) > $ deviceB 'sendEncryptedText' UserX | (Message) = < UserX | ('message' : Message , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , UserX : ('owner' : OldOwner , ..) , ...) , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; encrypt(R, Key)) = < cloudA | (deviceB : ('key' : Key , UserX : ('owner' : true , ..) , ...) , ....) > .`
- r4: `eq < cloudA | (deviceB : (UserX : ('owner' : true , ..) , ...) , ....) > $ UserX 'resetDevice' cloudA | (deviceB) = < cloudA | (deviceB : (UserX : ('owner' : nils , ..) , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

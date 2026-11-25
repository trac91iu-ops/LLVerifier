# Switchbot: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 7fb03a42e5a0.json (run1)

effect acc 85.7 rec 85.7; exact acc 57.1 rec 85.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |
| r2 |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 | exact (gen wider) |  |  |  |  |  |  |
| r7 |  | exact (gen wider) |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g6: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > $ UserX 'inviteUser' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > .`
- r5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 26f1b3a0718b.json (run2, run3, run5)

effect acc 85.7 rec 85.7; exact acc 57.1 rec 85.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |
| r2 |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 | exact (gen wider) |  |  |  |  |  |  |
| r7 |  | exact (gen wider) |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g6: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > .`
- r5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 214cbc2a1389.json (run3)

effect acc 85.7 rec 85.7; exact acc 85.7 rec 85.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |
| r2 |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 | exact |  |  |  |  |  |  |
| r7 |  | exact |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g6: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > .`
- r5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r6: `eq < UserX | ('near' : nils , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : deviceB , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 68adfca75785.json (run4)

effect acc 85.7 rec 85.7; exact acc 57.1 rec 85.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |
| r2 |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 | exact (gen wider) |  |  |  |  |  |  |
| r7 |  | exact (gen wider) |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g6: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > $ UserX 'inviteUser' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > .`
- r5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## d29610de83d0.json (run5)

effect acc 85.7 rec 85.7; exact acc 57.1 rec 85.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |
| r2 |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 | exact (gen wider) |  |  |  |  |  |  |
| r7 |  | exact (gen wider) |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g6: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : Owners , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owners' : (UserX , Owners) , ..) , ...) > .`
- r4: `eq < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > $ UserX 'inviteUser' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > .`
- r5: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (UserY , Members) , ..) , ...) > $ UserX 'removeUser' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

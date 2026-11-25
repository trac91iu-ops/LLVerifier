# Broadlink: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## c78e2acfa208.json (run1)

effect acc 66.7 rec 66.7; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | exact |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : randomStr('KeyB', N) , ...) > .`
- g4: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : nils , ...) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : KeyA , ...) > .`
- g5: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > $ UserX 'callAPI:lock' DeviceY | (KeyA) = < DeviceY | ('key' : KeyA , 'unlocked' : false , ..) > .`
- g6: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g7: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g8: `eq < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > $ UserY 'cloudAPI:getKey' cloudA | (DeviceY) < UserY | ('key' : KeyA , .....) > = < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > < UserY | ('key' : KeyA , .....) > .`
- g9: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) < cloudA | (DeviceY : ('owner' : SetA , ...) , ....) > = < cloudA | (DeviceY : ('owner' : (SetA , UserX) , ...) , ....) > < DeviceY | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : OldKey , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : randomStr('Key', N) , ...) > .`
- r4: `eq < UserX | ('key' : nils , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > $ UserX 'retrieveKey' deviceB = < UserX | ('key' : Key , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > .`
- r5: `eq < deviceB | ('locked' : false , 'key' : Key , ..) > $ UserX 'lock' deviceB | (Key) = < deviceB | ('locked' : true , 'key' : Key , ..) > .`
- r6: `eq < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : Owners , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : (UserX , Owners) , ...) , ....) > .`
- r7: `eq < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > $ userC 'invite' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > .`
- r8: `eq < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > $ userC 'remove' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r9: `eq < cloudA | (..) > $ UserY 'retrieveCloudKey' cloudA | (deviceB ; Key) = < cloudA | (..) > .`

## a394f17656e1.json (run2)

effect acc 66.7 rec 66.7; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | exact |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : randomStr('KeyB', N) , ...) > .`
- g4: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : nils , ...) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : KeyA , ...) > .`
- g5: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > $ UserX 'callAPI:lock' DeviceY | (KeyA) = < DeviceY | ('key' : KeyA , 'unlocked' : false , ..) > .`
- g6: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g7: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g8: `eq < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > $ UserY 'cloudAPI:getKey' cloudA | (DeviceY) < UserY | ('key' : KeyA , .....) > = < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > < UserY | ('key' : KeyA , .....) > .`
- g9: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) < cloudA | (DeviceY : ('owner' : SetA , ...) , ....) > = < cloudA | (DeviceY : ('owner' : (SetA , UserX) , ...) , ....) > < DeviceY | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : OldKey , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : randomStr('Key', N) , ...) > .`
- r4: `eq < UserX | ('key' : nils , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > $ UserX 'retrieveKey' deviceB = < UserX | ('key' : Key , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > .`
- r5: `eq < deviceB | ('locked' : false , 'key' : Key , ..) > $ UserX 'lock' deviceB | (Key) = < deviceB | ('locked' : true , 'key' : Key , ..) > .`
- r6: `eq < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : Owners , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : (UserX , Owners) , ...) , ....) > .`
- r7: `eq < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > $ userC 'invite' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > .`
- r8: `eq < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > $ userC 'remove' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r9: `eq < cloudA | (..) > $ UserY 'retrieveKey' cloudA | (deviceB) = < cloudA | (..) > .`

## 61f86da98a19.json (run3)

effect acc 66.7 rec 66.7; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | exact |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : randomStr('KeyB', N) , ...) > .`
- g4: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : nils , ...) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : KeyA , ...) > .`
- g5: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > $ UserX 'callAPI:lock' DeviceY | (KeyA) = < DeviceY | ('key' : KeyA , 'unlocked' : false , ..) > .`
- g6: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g7: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g8: `eq < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > $ UserY 'cloudAPI:getKey' cloudA | (DeviceY) < UserY | ('key' : KeyA , .....) > = < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > < UserY | ('key' : KeyA , .....) > .`
- g9: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) < cloudA | (DeviceY : ('owner' : SetA , ...) , ....) > = < cloudA | (DeviceY : ('owner' : (SetA , UserX) , ...) , ....) > < DeviceY | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : OldKey , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : randomStr('Key', N) , ...) > .`
- r4: `eq < UserX | ('key' : nils , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > $ UserX 'retrieveKey' deviceB = < UserX | ('key' : Key , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > .`
- r5: `eq < deviceB | ('locked' : false , 'key' : Key , ..) > $ UserX 'lock' deviceB | (Key) = < deviceB | ('locked' : true , 'key' : Key , ..) > .`
- r6: `eq < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : Owners , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : (UserX , Owners) , ...) , ....) > .`
- r7: `eq < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > $ userC 'invite' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > .`
- r8: `eq < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > $ userC 'remove' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r9: `eq < cloudA | (..) > $ UserY 'retrieveCloudKey' cloudA | (deviceB ; Key) = < cloudA | (..) > .`

## 004d27ab0cda.json (run4)

effect acc 66.7 rec 66.7; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | exact |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : randomStr('KeyB', N) , ...) > .`
- g4: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : nils , ...) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : KeyA , ...) > .`
- g5: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > $ UserX 'callAPI:lock' DeviceY | (KeyA) = < DeviceY | ('key' : KeyA , 'unlocked' : false , ..) > .`
- g6: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g7: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g8: `eq < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > $ UserY 'cloudAPI:getKey' cloudA | (DeviceY) < UserY | ('key' : KeyA , .....) > = < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > < UserY | ('key' : KeyA , .....) > .`
- g9: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) < cloudA | (DeviceY : ('owner' : SetA , ...) , ....) > = < cloudA | (DeviceY : ('owner' : (SetA , UserX) , ...) , ....) > < DeviceY | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : OldKey , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : randomStr('Key', N) , ...) > .`
- r4: `eq < UserX | ('key' : nils , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > $ UserX 'retrieveKey' deviceB = < UserX | ('key' : Key , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > .`
- r5: `eq < deviceB | ('locked' : false , 'key' : Key , ..) > $ UserX 'lock' deviceB | (Key) = < deviceB | ('locked' : true , 'key' : Key , ..) > .`
- r6: `eq < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : Owners , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : (UserX , Owners) , ...) , ....) > .`
- r7: `eq < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > $ userC 'invite' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > .`
- r8: `eq < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > $ userC 'remove' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > .`
- r9: `eq < cloudA | (..) > $ UserY 'retrieveCloudKey' cloudA | (deviceB ; Key) = < cloudA | (..) > .`

## 7892ce3e0d34.json (run5)

effect acc 66.7 rec 66.7; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | exact |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | ('key' : KeyA , ...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | ('key' : randomStr('KeyB', N) , ...) > .`
- g4: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : nils , ...) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > < UserX | ('key' : KeyA , ...) > .`
- g5: `eq < DeviceY | ('key' : KeyA , 'unlocked' : true , ..) > $ UserX 'callAPI:lock' DeviceY | (KeyA) = < DeviceY | ('key' : KeyA , 'unlocked' : false , ..) > .`
- g6: `eq < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > .`
- g7: `eq < cloudA | (UserX : ('devices' : nils , 'members' : (SetA , UserY) , ..) , ...) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('devices' : nils , 'members' : SetA , ..) , ...) > .`
- g8: `eq < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > $ UserY 'cloudAPI:getKey' cloudA | (DeviceY) < UserY | ('key' : KeyA , .....) > = < cloudA | (DeviceY : ('key' : KeyA , ..) , ...) > < UserX | ('members' : (SetA , UserY) , ....) > < UserY | ('key' : KeyA , .....) > .`
- g9: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) < cloudA | (DeviceY : ('owner' : SetA , ...) , ....) > = < cloudA | (DeviceY : ('owner' : (SetA , UserX) , ...) , ....) > < DeviceY | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | ('key' : OldKey , ...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | ('key' : randomStr('Key', N) , ...) > .`
- r4: `eq < UserX | ('key' : nils , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > $ UserX 'retrieveKey' deviceB = < UserX | ('key' : Key , ..) > < deviceB | ('locked' : false , 'key' : Key , ...) > .`
- r5: `eq < deviceB | ('locked' : false , 'key' : Key , ..) > $ UserX 'lock' deviceB | (Key) = < deviceB | ('locked' : true , 'key' : Key , ..) > .`
- r6: `eq < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : Owners , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < deviceB | ('key' : Key , ..) > < cloudA | (deviceB : ('owners' : (UserX , Owners) , ...) , ....) > .`
- r7: `eq < cloudA | (userC : ('devices' : nils , 'members' : Members , ..) , ...) > $ userC 'invite' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : (userA , Members) , ..) , ...) > .`
- r8: `eq < cloudA | (userC : ('devices' : nils , 'members' : (userA , Rest) , ..) , ...) > $ userC 'remove' cloudA | (userA) = < cloudA | (userC : ('devices' : nils , 'members' : Rest , ..) , ...) > .`
- r9: `eq < cloudA | (..) > $ UserY 'retrieveCloudKey' cloudA | (deviceB ; Key) = < cloudA | (..) > .`

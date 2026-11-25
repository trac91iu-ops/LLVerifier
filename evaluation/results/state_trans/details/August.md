# August: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## d49711e476b3.json (run1)

effect acc 100.0 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |
| r3 |  |  | exact (gen wider) |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  | exact |  |
| r7 |  |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , 'online' : false , 'key' : KeyA , 'owner' : nils , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , 'online' : true , 'key' : KeyA , 'owner' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : nils , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : UserX , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY) = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' DeviceY .`
- g7: `eq < DeviceY | ('online' : true , 'owner' : UserX , ..) > $ cloudA 'resetDevice' DeviceY = < DeviceY | ('online' : false , 'owner' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('owner' : nils , 'online' : false , 'buttonPressed' : OldPressed , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('owner' : nils , 'online' : true , 'buttonPressed' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > < deviceB | ('owner' : nils , 'online' : true , 'key' : Key , ....) > $ UserX 'callAPI:bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > < deviceB | ('owner' : UserX , 'online' : true , 'key' : Key , ....) > .`
- r6: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > $ cloudA 'reset' deviceB .`
- r7: `eq < deviceB | ('online' : true , 'owner' : UserOwner , ..) > $ cloudA 'reset' deviceB = < deviceB | ('online' : false , 'owner' : nils , ..) > .`

## 63d22685cfc3.json (run2)

effect acc 71.4 rec 71.4; exact acc 28.6 rec 71.4

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |
| r3 |  |  | exact (gen wider) |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , 'online' : false , 'key' : KeyA , 'owner' : nils , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , 'online' : true , 'key' : KeyA , 'owner' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : nils , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : UserX , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY) = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' DeviceY .`
- g7: `eq < DeviceY | ('online' : true , 'owner' : UserX , ..) > $ cloudA 'resetDevice' DeviceY = < DeviceY | ('online' : false , 'owner' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('owner' : nils , 'online' : false , 'buttonPressed' : OldPressed , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('owner' : nils , 'online' : true , 'buttonPressed' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > < deviceB | ('owner' : nils , 'online' : true , 'key' : Key , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > < deviceB | ('owner' : UserX , 'online' : true , 'key' : Key , ....) > .`
- r6: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > $ cloudA 'reset' deviceB .`
- r7: `eq < deviceB | ('online' : true , 'owner' : UserOwner , ..) > $ cloudA 'reset' deviceB = < deviceB | ('online' : false , 'owner' : nils , ..) > .`

## 8e4dcafbbe76.json (a2-run2)

effect acc 100.0 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |
| r3 |  |  | exact (gen wider) |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  | exact |  |
| r7 |  |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , 'online' : false , 'key' : KeyA , 'owner' : nils , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , 'online' : true , 'key' : KeyA , 'owner' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : nils , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : UserX , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY) = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' DeviceY .`
- g7: `eq < DeviceY | ('online' : true , 'owner' : UserX , ..) > $ cloudA 'resetDevice' DeviceY = < DeviceY | ('online' : false , 'owner' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('owner' : nils , 'online' : false , 'buttonPressed' : OldPressed , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('owner' : nils , 'online' : true , 'buttonPressed' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > < deviceB | ('owner' : nils , 'online' : true , 'key' : Key , ....) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > < deviceB | ('owner' : UserX , 'online' : true , 'key' : Key , ....) > .`
- r6: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' deviceB .`
- r7: `eq < deviceB | ('online' : true , 'owner' : UserOwner , ..) > $ cloudA 'resetDevice' deviceB = < deviceB | ('online' : false , 'owner' : nils , ..) > .`

## a144c22c4524.json (run4)

effect acc 100.0 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |
| r3 |  |  | exact (gen wider) |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  | exact |  |
| r7 |  |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , 'online' : false , 'key' : KeyA , 'owner' : nils , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , 'online' : true , 'key' : KeyA , 'owner' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : nils , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : UserX , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY) = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' DeviceY .`
- g7: `eq < DeviceY | ('online' : true , 'owner' : UserX , ..) > $ cloudA 'resetDevice' DeviceY = < DeviceY | ('online' : false , 'owner' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('owner' : nils , 'online' : false , 'buttonPressed' : OldPressed , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('owner' : nils , 'online' : true , 'buttonPressed' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > < deviceB | ('owner' : nils , 'online' : true , 'key' : Key , ....) > $ UserX 'callAPI:bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > < deviceB | ('owner' : UserX , 'online' : true , 'key' : Key , ....) > .`
- r6: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > $ cloudA 'reset' deviceB .`
- r7: `eq < deviceB | ('online' : true , 'owner' : UserOwner , ..) > $ cloudA 'reset' deviceB = < deviceB | ('online' : false , 'owner' : nils , ..) > .`

## 6ad46dba8686.json (run5)

effect acc 100.0 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 |
|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |
| r3 |  |  | exact (gen wider) |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |
| r5 |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  | exact |  |
| r7 |  |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , 'online' : false , 'key' : KeyA , 'owner' : nils , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , 'online' : true , 'key' : KeyA , 'owner' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : nils , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , 'key' : KeyA , 'owner' : UserX , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY) = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > $ cloudA 'resetDevice' DeviceY .`
- g7: `eq < DeviceY | ('online' : true , 'owner' : UserX , ..) > $ cloudA 'resetDevice' DeviceY = < DeviceY | ('online' : false , 'owner' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('owner' : nils , 'online' : false , 'buttonPressed' : OldPressed , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('owner' : nils , 'online' : true , 'buttonPressed' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > < deviceB | ('owner' : nils , 'online' : true , 'key' : Key , ....) > $ UserX 'callAPI:bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > < deviceB | ('owner' : UserX , 'online' : true , 'key' : Key , ....) > .`
- r6: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > $ cloudA 'reset' deviceB .`
- r7: `eq < deviceB | ('online' : true , 'owner' : UserY , ..) > $ cloudA 'reset' deviceB = < deviceB | ('online' : false , 'owner' : nils , ..) > .`

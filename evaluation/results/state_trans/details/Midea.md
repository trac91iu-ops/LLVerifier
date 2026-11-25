# Midea: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## f52f5ffec3d5.json (run1, run3, run4, run5)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('key' : KeyA , 'online' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , 'online' : true , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g2: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g3: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , ....) > .`
- g4: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > < DeviceY | ('online' : false , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('online' : false , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('online' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > < deviceB | ('online' : true , ....) > .`
- r4: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'resetDevice' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > < deviceB | ('online' : false , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 2f520d052eac.json (a2-run2, a2-run4)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('key' : KeyA , 'online' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , 'online' : true , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g2: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g3: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , ....) > .`
- g4: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:reset' cloudA = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > < DeviceY | ('online' : false , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('online' : false , 'key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('online' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > < deviceB | ('online' : true , ....) > .`
- r4: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'resetDevice' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > < deviceB | ('online' : false , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

# Imou: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 163fbaa108ef.json (run1, run3)

effect acc 100.0 rec 83.3; exact acc 100.0 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 |  | exact |  |  |  |  |
| r2 |  |  | exact |  |  |  |
| r3 |  |  |  | exact |  |  |
| r4 |  |  |  |  | exact |  |
| r5 |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , 'online' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , 'online' : true , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('owner' : nils , 'bdKey' : KeyA , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:bind' cloudA | (KeyA) = < cloudA | (DeviceY : ('owner' : UserX , 'bdKey' : KeyA , ..) , ...) > < DeviceY | ('online' : true , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA < DeviceY | ('online' : false , ....) > = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > < DeviceY | ('online' : false , ....) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r2: `eq < deviceB | ('online' : false , 'key' : Key , ..) > $ UserX 'buttonPress' deviceB = < deviceB | ('online' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r3: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r4: `eq < cloudA | (deviceB : ('owner' : nils , 'bindingKey' : Key , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'bind' cloudA | (Key) = < cloudA | (deviceB : ('owner' : UserX , 'bindingKey' : Key , ..) , ...) > < deviceB | ('online' : true , ....) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > < deviceB | ('online' : false , ....) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > < deviceB | ('online' : false , ....) > .`

## ddebe3c65b5d.json (run2, run4, run5)

effect acc 100.0 rec 83.3; exact acc 100.0 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 |  | exact |  |  |  |  |
| r2 |  |  | exact |  |  |  |
| r3 |  |  |  | exact |  |  |
| r4 |  |  |  |  | exact |  |
| r5 |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , 'online' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , 'online' : true , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('owner' : nils , 'bdKey' : KeyA , ..) , ...) > < DeviceY | ('online' : true , ....) > $ UserX 'callAPI:bind' cloudA | (KeyA) = < cloudA | (DeviceY : ('owner' : UserX , 'bdKey' : KeyA , ..) , ...) > < DeviceY | ('online' : true , ....) > .`
- g6: `eq < cloudA | (DeviceY : ('owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA < DeviceY | ('online' : false , ....) > = < cloudA | (DeviceY : ('owner' : nils , ..) , ...) > < DeviceY | ('online' : false , ....) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : deviceB , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r2: `eq < deviceB | ('online' : false , 'key' : Key , ..) > $ UserX 'buttonPress' deviceB = < deviceB | ('online' : true , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r3: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r4: `eq < cloudA | (deviceB : ('owner' : nils , 'bindingKey' : Key , ..) , ...) > < deviceB | ('online' : true , ....) > $ UserX 'bind' cloudA | (Key) = < cloudA | (deviceB : ('owner' : UserX , 'bindingKey' : Key , ..) , ...) > < deviceB | ('online' : true , ....) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : UserX , ..) , ...) > < deviceB | ('online' : false , ....) > $ UserX 'reset' cloudA | (deviceB) = < cloudA | (deviceB : ('owner' : nils , ..) , ...) > < deviceB | ('online' : false , ....) > .`

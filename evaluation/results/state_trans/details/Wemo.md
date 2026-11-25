# Wemo: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 343ddf18e04f.json (a2-run3)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact (gen narrower) |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'press' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('key' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('key' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## f845a3c83cd0.json (run2, run3)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact (gen narrower) |  |  |  |  |
| r3 |  |  | exact (gen narrower) |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'press' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < cloudA | (UserX : ('key' : Key , ..) , ...) > < deviceB | ('buttonPressed' : true , 'key' : nils , ....) > $ UserX 'sendKey' deviceB | (Key) = < cloudA | (UserX : ('key' : Key , ..) , ...) > < deviceB | ('buttonPressed' : false , 'key' : Key , ....) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('key' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('key' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 98a1e6e20c99.json (run4)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact (gen narrower) |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'press' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 089cedb420ba.json (run5)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact (gen narrower) |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen wider) |  |
| r6 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'press' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

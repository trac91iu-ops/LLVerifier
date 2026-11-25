# CloudEdgeRTE: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## afbd12553c10.json (run1)

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
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'presses' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g5: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g6: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' DeviceX = < UserX | ('near' : DeviceX , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' DeviceX = < UserX | ('near' : nils , ..) > .`
- r3: `eq < DeviceX | ('buttonPressed' : false , ..) > $ UserX 'pressButton' DeviceX = < DeviceX | ('buttonPressed' : true , ..) > .`
- r4: `eq < DeviceX | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' DeviceX | (Key) = < DeviceX | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r5: `ceq < DeviceX | ('key' : Key , ..) > $ UserX 'discover' DeviceX = < DeviceX | ('key' : Key , ..) > $ DeviceX 'bind' cloudA | (DeviceX ; Key) if Key =/= nils .`
- r6: `eq < cloudA | (UserY : ('key' : Key , ..) , DeviceX : ('owner' : nils , ...) , ....) > $ DeviceX 'bind' cloudA | (DeviceX ; Key) = < cloudA | (UserY : ('key' : Key , ..) , DeviceX : ('owner' : UserY , ...) , ....) > .`

## 76a8c926e2fd.json (run5)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen narrower) |  |
| r6 |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'presses' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g5: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g6: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' DeviceX = < UserX | ('near' : DeviceX , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' DeviceX = < UserX | ('near' : nils , ..) > .`
- r3: `eq < DeviceX | ('buttonPressed' : false , ..) > $ UserX 'pressButton' DeviceX = < DeviceX | ('buttonPressed' : true , ..) > .`
- r4: `eq < DeviceX | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' DeviceX | (Key) = < DeviceX | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r5: `ceq < DeviceX | ('key' : Key , ..) > $ UserX 'discover' DeviceX = < DeviceX | ('key' : Key , ..) > $ DeviceX 'bind' cloudA | (Key) if Key =/= nils .`
- r6: `eq < cloudA | (DeviceX : ('owner' : nils , ..) , UserY : ('key' : Key , ...) , ....) > $ DeviceX 'bind' cloudA | (Key) = < cloudA | (DeviceX : ('owner' : UserY , ..) , UserY : ('key' : Key , ...) , ....) > .`

## 6afe44712c0b.json (run1)

effect acc 100.0 rec 100.0; exact acc 66.7 rec 83.3

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  | exact |  |  |
| r5 |  |  |  |  | exact (gen narrower) |  |
| r6 |  |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'presses' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g5: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g6: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' DeviceX = < UserX | ('near' : DeviceX , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' DeviceX = < UserX | ('near' : nils , ..) > .`
- r3: `eq < DeviceX | ('buttonPressed' : false , ..) > $ UserX 'pressButton' DeviceX = < DeviceX | ('buttonPressed' : true , ..) > .`
- r4: `eq < DeviceX | ('buttonPressed' : true , 'key' : nils , ..) > $ UserX 'sendKey' DeviceX | (Key) = < DeviceX | ('buttonPressed' : false , 'key' : Key , ..) > .`
- r5: `ceq < DeviceX | ('key' : Key , ..) > $ UserX 'discover' DeviceX = < DeviceX | ('key' : Key , ..) > $ DeviceX 'bind' cloudA | (Key) if Key =/= nils .`
- r6: `eq < cloudA | (DeviceX : ('owner' : nils , ..) , UserY : ('key' : Key , ...) , ....) > $ DeviceX 'bind' cloudA | (Key) = < cloudA | (DeviceX : ('owner' : UserY , ..) , UserY : ('key' : Key , ...) , ....) > .`

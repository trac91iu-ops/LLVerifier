# TPLink: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 5bc65cbf39eb.json (a2-run4)

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

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
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

## 4c498f3b4fad.json (run2)

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

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < cloudA | (UserX : ('accountKey' : Key , ..) , ...) > < deviceB | ('buttonPressed' : true , 'key' : nils , ....) > $ UserX 'sendKey' deviceB | (Key) = < cloudA | (UserX : ('accountKey' : Key , ..) , ...) > < deviceB | ('buttonPressed' : false , 'key' : Key , ....) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## f845a3c83cd0.json (run3, run4)

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

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
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

## f63e307565f6.json (run3)

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

- g1: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g2: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'callAPI:discover' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) .`
- g4: `eq < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : nils , ...) , ....) > $ DeviceY 'callAPI:bind' cloudA | (KeyA) = < cloudA | (UserX : ('key' : KeyA , ..) , DeviceY : ('owner' : UserX , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < cloudA | (UserX : ('accountKey' : Key , ..) , ...) > < deviceB | ('buttonPressed' : true , 'key' : nils , ....) > $ UserX 'sendKey' deviceB | (Key) = < cloudA | (UserX : ('accountKey' : Key , ..) , ...) > < deviceB | ('buttonPressed' : false , 'key' : Key , ....) > .`
- r3: `ceq < deviceB | ('key' : Key , ..) > $ UserX 'discover' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'bind' cloudA | (deviceB ; Key) if Key =/= nils .`
- r4: `eq < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : nils , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Key) = < cloudA | (UserY : ('accountKey' : Key , ..) , deviceB : ('owner' : UserY , ...) , ....) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

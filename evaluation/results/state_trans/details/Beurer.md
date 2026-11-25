# Beurer: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## ce2b1045c047.json (run1)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |
| r3 |  |  | exact |  |  |
| r4 |  |  |  | exact |  |
| r5 |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > .`

## bec407aa8776.json (run5)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |
| r3 |  |  | exact |  |  |
| r4 |  |  |  | exact |  |
| r5 |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > .`

## 2eb0c3b1dc7c.json (a2-run3, a2-run5)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |
| r3 |  |  | exact |  |  |
| r4 |  |  |  | exact |  |
| r5 |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > .`

## ce80f714964b.json (run1, run3, run4)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |
| r3 |  |  | exact |  |  |
| r4 |  |  |  | exact |  |
| r5 |  |  |  |  | exact |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < cloudA | (deviceB : ('owner' : nils , 'key' : Key , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('owner' : UserX , 'key' : Key , ..) , ...) > .`

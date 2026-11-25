# Sunlogin: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## d1ecfd3f32cc.json (a2-run4)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |
| r2 |  |  |  | exact |  |
| r3 |  |  |  |  | exact |
| r4 | exact (gen wider) |  |  |  |  |
| r5 |  | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , 'key' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , 'key' : nils , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'send' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > .`
- r4: `eq < UserX | ('key' : nils , 'near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('key' : nils , 'near' : deviceB , ..) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## a7ca3439a688.json (run2)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |
| r2 |  |  |  | exact |  |
| r3 |  |  |  |  | exact |
| r4 | exact (gen wider) |  |  |  |  |
| r5 |  | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , 'key' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , 'key' : nils , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'send' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > .`
- r4: `eq < UserX | ('key' : nils , 'near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('key' : nils , 'near' : deviceB , ..) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## ccee4f44af77.json (run5)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |
| r2 |  |  |  | exact |  |
| r3 |  |  |  |  | exact |
| r4 | exact (gen wider) |  |  |  |  |
| r5 |  | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , 'key' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , 'key' : nils , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'send' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > .`
- r4: `eq < UserX | ('key' : nils , 'near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('key' : nils , 'near' : deviceB , ..) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 1891811a1a70.json (a2-run3)

effect acc 100.0 rec 100.0; exact acc 60.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 |
|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |
| r2 |  |  |  | exact |  |
| r3 |  |  |  |  | exact |
| r4 | exact (gen wider) |  |  |  |  |
| r5 |  | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , 'key' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , 'key' : nils , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('key' : KeyA , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('key' : KeyA , ..) > $ DeviceY 'send' UserX | (KeyA) .`
- g4: `eq < UserX | ('key' : nils , ..) > $ DeviceY 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g5: `eq < cloudA | (DeviceY : ('key' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('key' : KeyA , 'owner' : UserX , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Key , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Key , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) .`
- r2: `eq < UserX | ('key' : nils , ..) > $ deviceB 'sendDeviceKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < cloudA | (deviceB : ('key' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('key' : Key , 'owner' : UserX , ..) , ...) > .`
- r4: `eq < UserX | ('key' : nils , 'near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('key' : nils , 'near' : deviceB , ..) > .`
- r5: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

# Meross: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## e71bdebfcb7b.json (run1)

effect acc 85.7 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 |  |  |  | exact |  |  |
| r6 |  |  |  |  | exact (gen wider) |  |
| r7 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'pressButton' DeviceX = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'sendKey' UserY | (KeyA) .`
- g2: `eq < UserX | ('keys' : SetA , ..) > $ DeviceY 'sendKey' UserX | (KeyB) = < UserX | ('keys' : (SetA , KeyB) , ..) > .`
- g3: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'callAPI:bind' DeviceX | (KeyB) = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'callAPI:bind' cloudA | (KeyA ; KeyB) .`
- g4: `eq < cloudA | (DeviceX : ('key' : KeyA , 'owner' : nils , ..) , UserY : ('key' : KeyB , ...) , ....) > $ AnyPrincipal 'callAPI:bind' cloudA | (KeyA ; KeyB) = < cloudA | (DeviceX : ('key' : KeyA , 'owner' : UserY , ..) , UserY : ('key' : KeyB , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) .`
- r2: `eq < UserX | ('keys' : Keys , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) = < UserX | ('keys' : (Kdevice , Keys) , ..) > .`
- r3: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'bindDevice' deviceB | (Kuser) = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'bindCloud' cloudA | (deviceB ; Kdevice ; Kuser) .`
- r4: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ deviceB 'bindCloud' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ UserX 'bindCloud' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 4ed2c488cf4e.json (run2)

effect acc 85.7 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 |  |  |  | exact |  |  |
| r6 |  |  |  |  | exact (gen wider) |  |
| r7 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'pressButton' DeviceX = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'sendKey' UserY | (KeyA) .`
- g2: `eq < UserX | ('keys' : SetA , ..) > $ DeviceY 'sendKey' UserX | (KeyB) = < UserX | ('keys' : (SetA , KeyB) , ..) > .`
- g3: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'callAPI:bind' DeviceX | (KeyB) = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'callAPI:bind' cloudA | (KeyA ; KeyB) .`
- g4: `eq < cloudA | (DeviceX : ('key' : KeyA , 'owner' : nils , ..) , UserY : ('key' : KeyB , ...) , ....) > $ AnyPrincipal 'callAPI:bind' cloudA | (KeyA ; KeyB) = < cloudA | (DeviceX : ('key' : KeyA , 'owner' : UserY , ..) , UserY : ('key' : KeyB , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) .`
- r2: `eq < UserX | ('keys' : Keys , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) = < UserX | ('keys' : (Kdevice , Keys) , ..) > .`
- r3: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'bindDevice' deviceB | (Kuser) = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) .`
- r4: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 3498a3914e68.json (run3)

effect acc 85.7 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 |  |  |  | exact |  |  |
| r6 |  |  |  |  | exact (gen wider) |  |
| r7 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'pressButton' DeviceX = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'sendKey' UserY | (KeyA) .`
- g2: `eq < UserX | ('keys' : SetA , ..) > $ DeviceY 'sendKey' UserX | (KeyB) = < UserX | ('keys' : (SetA , KeyB) , ..) > .`
- g3: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'callAPI:bind' DeviceX | (KeyB) = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'callAPI:bind' cloudA | (KeyA ; KeyB) .`
- g4: `eq < cloudA | (DeviceX : ('key' : KeyA , 'owner' : nils , ..) , UserY : ('key' : KeyB , ...) , ....) > $ AnyPrincipal 'callAPI:bind' cloudA | (KeyA ; KeyB) = < cloudA | (DeviceX : ('key' : KeyA , 'owner' : UserY , ..) , UserY : ('key' : KeyB , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) .`
- r2: `eq < UserX | ('keys' : Keys , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) = < UserX | ('keys' : (Kdevice , Keys) , ..) > .`
- r3: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'bindDevice' deviceB | (Kuser) = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) .`
- r4: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 69d0ad5d10f2.json (run4)

effect acc 85.7 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 |  |  |  | exact |  |  |
| r6 |  |  |  |  | exact (gen wider) |  |
| r7 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'pressButton' DeviceX = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'sendKey' UserY | (KeyA) .`
- g2: `eq < UserX | ('keys' : SetA , ..) > $ DeviceY 'sendKey' UserX | (KeyB) = < UserX | ('keys' : (SetA , KeyB) , ..) > .`
- g3: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'callAPI:bind' DeviceX | (KeyB) = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'callAPI:bind' cloudA | (KeyA ; KeyB) .`
- g4: `eq < cloudA | (DeviceX : ('key' : KeyA , 'owner' : nils , ..) , UserY : ('key' : KeyB , ...) , ....) > $ AnyPrincipal 'callAPI:bind' cloudA | (KeyA ; KeyB) = < cloudA | (DeviceX : ('key' : KeyA , 'owner' : UserY , ..) , UserY : ('key' : KeyB , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) .`
- r2: `eq < UserX | ('keys' : Keys , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) = < UserX | ('keys' : (Kdevice , Keys) , ..) > .`
- r3: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'bindDevice' deviceB | (Kuser) = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) .`
- r4: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ deviceB 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ UserX 'bindDevice' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 2cb48d43a42d.json (run2)

effect acc 85.7 rec 100.0; exact acc 57.1 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 |
|---|---|---|---|---|---|---|
| r1 | exact |  |  |  |  |  |
| r2 |  | exact |  |  |  |  |
| r3 |  |  | exact |  |  |  |
| r4 |  |  |  |  |  |  |
| r5 |  |  |  | exact |  |  |
| r6 |  |  |  |  | exact (gen wider) |  |
| r7 |  |  |  |  |  | exact (gen wider) |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'pressButton' DeviceX = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'sendKey' UserY | (KeyA) .`
- g2: `eq < UserX | ('keys' : SetA , ..) > $ DeviceY 'sendKey' UserX | (KeyB) = < UserX | ('keys' : (SetA , KeyB) , ..) > .`
- g3: `eq < DeviceX | ('key' : KeyA , ..) > $ UserY 'callAPI:bind' DeviceX | (KeyB) = < DeviceX | ('key' : KeyA , ..) > $ DeviceX 'callAPI:bind' cloudA | (KeyA ; KeyB) .`
- g4: `eq < cloudA | (DeviceX : ('key' : KeyA , 'owner' : nils , ..) , UserY : ('key' : KeyB , ...) , ....) > $ AnyPrincipal 'callAPI:bind' cloudA | (KeyA ; KeyB) = < cloudA | (DeviceX : ('key' : KeyA , 'owner' : UserY , ..) , UserY : ('key' : KeyB , ...) , ....) > .`
- g5: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g6: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) .`
- r2: `eq < UserX | ('keys' : Keys , ..) > $ deviceB 'sendDeviceKey' UserX | (Kdevice) = < UserX | ('keys' : (Kdevice , Keys) , ..) > .`
- r3: `eq < deviceB | ('key' : Kdevice , ..) > $ UserX 'bindDevice' deviceB | (Kuser) = < deviceB | ('key' : Kdevice , ..) > $ deviceB 'bind' cloudA | (deviceB ; Kdevice ; Kuser) .`
- r4: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ deviceB 'bind' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r5: `eq < cloudA | (deviceB : ('key' : Kdevice , 'owner' : nils , ..) , UserY : ('key' : Kuser , ...) , ....) > $ UserX 'bind' cloudA | (deviceB ; Kdevice ; Kuser) = < cloudA | (deviceB : ('key' : Kdevice , 'owner' : UserY , ..) , UserY : ('key' : Kuser , ...) , ....) > .`
- r6: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r7: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

# TuyaCAC: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 041ec2a25554.json (run1)

effect acc 100.0 rec 100.0; exact acc 71.4 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | effect |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | effect |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'status' : false , ..) > $ UserY 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'status' : true , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('device' : DeviceY , 'members' : (SetA , UserZ) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , UserZ) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > $ UserX 'callAPI:kick' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserY | (KeyA) .`
- g7: `eq < DeviceX | ('status' : false , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('status' : true , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOnWithKey' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'turnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : DeviceY , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 3f1d810d8300.json (run1, run3)

effect acc 100.0 rec 100.0; exact acc 71.4 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | effect |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | effect |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'status' : false , ..) > $ UserY 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'status' : true , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('device' : DeviceY , 'members' : (SetA , UserZ) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , UserZ) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > $ UserX 'callAPI:kick' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserY | (KeyA) .`
- g7: `eq < DeviceX | ('status' : false , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('status' : true , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOn' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'cloudTurnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceY , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 6bac143dcaf2.json (run3)

effect acc 100.0 rec 100.0; exact acc 71.4 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | effect |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | effect |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'status' : false , ..) > $ UserY 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'status' : true , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('device' : DeviceY , 'members' : (SetA , UserZ) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , UserZ) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > $ UserX 'callAPI:kick' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserY | (KeyA) .`
- g7: `eq < DeviceX | ('status' : false , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('status' : true , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > < DeviceX | (.....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : DeviceX , ...) , ....) > < DeviceX | (.....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOnWithKey' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'turnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : DeviceY , ...) , ....) > < DeviceY | (.....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : nils , ...) , ....) > < DeviceY | (.....) > .`

## dae45edceb85.json (run4)

effect acc 100.0 rec 100.0; exact acc 71.4 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | effect |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | effect |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'status' : false , ..) > $ UserY 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'status' : true , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('device' : DeviceY , 'members' : (SetA , UserZ) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , UserZ) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > $ UserX 'callAPI:kick' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserY | (KeyA) .`
- g7: `eq < DeviceX | ('status' : false , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('status' : true , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOnWithKey' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'turnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceY , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 04681866a6e0.json (run5)

effect acc 100.0 rec 100.0; exact acc 71.4 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | effect |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | effect |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'status' : false , ..) > $ UserY 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'status' : true , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('device' : DeviceY , 'members' : (SetA , UserZ) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceY , 'members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , UserZ) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserZ , SetA , ..) , ...) , UserZ : ('device' : DeviceY , ....) , .....) > $ UserX 'callAPI:kick' cloudA | (UserZ) = < cloudA | (UserX : ('members' : (SetA , ..) , ...) , UserZ : ('device' : nils , ....) , .....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserY | (KeyA) .`
- g7: `eq < DeviceX | ('status' : false , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > $ UserY 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('status' : true , ..) > < cloudA | (UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Rest) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Rest) , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > < deviceB | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > < deviceB | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (deviceB ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (deviceB ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < deviceB | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOn' deviceB | (Key) = < deviceB | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > < deviceB | ('on' : false , ....) > $ UserX 'cloudTurnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > < deviceB | ('on' : true , ....) > .`
- r7: `ceq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : AssociatedDevice , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > if AssociatedDevice =/= nils .`

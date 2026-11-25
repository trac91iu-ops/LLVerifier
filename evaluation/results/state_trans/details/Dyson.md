# Dyson: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## bba808210b35.json (run3)

effect acc 100.0 rec 100.0; exact acc 100.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'state' : 'off' , ..) > $ UserX 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'state' : 'on' , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : DeviceX , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserY , SetA) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA) , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserX | (KeyA) .`
- g7: `eq < DeviceX | ('state' : 'off' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('state' : 'on' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOn' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'cloudTurnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## f1098b892d26.json (run2)

effect acc 100.0 rec 100.0; exact acc 100.0 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'state' : 'off' , ..) > $ UserX 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'state' : 'on' , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : DeviceX , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserY , SetA) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA) , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserX | (KeyA) .`
- g7: `eq < DeviceX | ('state' : 'off' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('state' : 'on' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOn' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'cloudTurnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## f124f2fb7556.json (run4)

effect acc 100.0 rec 100.0; exact acc 100.0 rec 75.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  | exact (gen wider) |  | exact |  |  |  |  |
| r2 |  |  | exact (gen narrower) |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |
| r4 |  |  |  |  |  |  |  | exact |
| r5 | exact |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  | exact |  |
| r7 |  |  |  |  | exact (gen narrower) |  |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : KeyA , 'state' : 'off' , ..) > $ UserX 'callAPI:toggle' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'state' : 'on' , ..) > .`
- g2: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , ...) > .`
- g3: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : nils , ....) , .....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , ..) , ...) , UserY : ('device' : DeviceX , ....) , .....) > .`
- g4: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (UserX : ('members' : (UserY , SetA) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA) , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g6: `eq < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:getKey' cloudA | (DeviceX) = < DeviceX | ('key' : KeyA , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ cloudA 'send' UserX | (KeyA) .`
- g7: `eq < DeviceX | ('state' : 'off' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > $ UserX 'cloudAPI:toggle' cloudA | (DeviceX) = < DeviceX | ('state' : 'on' , ..) > < cloudA | (UserX : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < UserX | ('key' : nils , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `ceq < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (UserY , Members) , ..) , UserY : ('device' : DeviceX , ...) , ....) > if DeviceX =/= nils .`
- r3: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ UserX 'requestKey' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('key' : Key , ....) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) .`
- r4: `eq < UserX | ('key' : nils , ..) > $ cloudA 'sendKey' UserX | (DeviceX ; Key) = < UserX | ('key' : Key , ..) > .`
- r5: `eq < DeviceX | ('key' : Key , 'on' : false , ..) > $ UserX 'turnOn' DeviceX | (Key) = < DeviceX | ('key' : Key , 'on' : true , ..) > .`
- r6: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : false , ....) > $ UserX 'cloudTurnOn' cloudA | (DeviceX) = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > < DeviceX | ('on' : true , ....) > .`
- r7: `ceq < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : nils , ...) , ....) > if DeviceX =/= nils .`

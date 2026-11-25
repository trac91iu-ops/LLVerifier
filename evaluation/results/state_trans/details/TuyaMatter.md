# TuyaMatter: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 29c0e97a19e6.json (run1)

effect acc 88.9 rec 100.0; exact acc 88.9 rec 100.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  | exact |  |  |  |
| r2 |  |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  | exact |
| r4 | exact |  |  |  |  |  |  |  |
| r5 |  | exact |  |  |  |  |  |  |
| r6 |  |  | exact |  |  |  |  |  |
| r7 |  |  |  | exact |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  | exact |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : nils , ..) > $ cloudA 'callAPI:openWindow' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , ..) > .`
- g2: `eq < DeviceX | ('key' : KeyA , 'trustSet' : SetA , ..) > $ UserX 'callAPI:bind' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'trustSet' : (SetA , UserX) , ..) > .`
- g3: `eq < DeviceX | ('on' : false , 'trustSet' : (SetA , PrincipalX) , ...) > $ PrincipalX 'callAPI:toggle' DeviceX = < DeviceX | ('on' : true , 'trustSet' : (SetA , PrincipalX) , ...) > .`
- g4: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ UserX 'cloudAPI:toggle' cloudA = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ cloudA 'callAPI:toggle' DeviceX .`
- g5: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g6: `eq < cloudA | (UserX : ('members' : (SetA , UserY) , 'device' : DeviceX , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : SetA , 'device' : DeviceX , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g7: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ UserX 'callAPI:openWindow' cloudA | (DeviceX) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('KeyA', N) , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ cloudA 'callAPI:openWindow' DeviceX | (randomStr('KeyA', N)) .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r3: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r4: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r5: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r6: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'cloudTurnOn' cloudA = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r8: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r9: `eq < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > .`

## d3b0ddf802ee.json (run2)

effect acc 70.0 rec 87.5; exact acc 70.0 rec 87.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  | exact |  |  |  |
| r2 |  |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  | exact |
| r4 | exact |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  | exact |  |  |  |  |  |  |
| r7 |  |  | exact |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |
| r10 |  |  |  |  |  | exact |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : nils , ..) > $ cloudA 'callAPI:openWindow' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , ..) > .`
- g2: `eq < DeviceX | ('key' : KeyA , 'trustSet' : SetA , ..) > $ UserX 'callAPI:bind' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'trustSet' : (SetA , UserX) , ..) > .`
- g3: `eq < DeviceX | ('on' : false , 'trustSet' : (SetA , PrincipalX) , ...) > $ PrincipalX 'callAPI:toggle' DeviceX = < DeviceX | ('on' : true , 'trustSet' : (SetA , PrincipalX) , ...) > .`
- g4: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ UserX 'cloudAPI:toggle' cloudA = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ cloudA 'callAPI:toggle' DeviceX .`
- g5: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g6: `eq < cloudA | (UserX : ('members' : (SetA , UserY) , 'device' : DeviceX , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : SetA , 'device' : DeviceX , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g7: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ UserX 'callAPI:openWindow' cloudA | (DeviceX) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('KeyA', N) , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ cloudA 'callAPI:openWindow' DeviceX | (randomStr('KeyA', N)) .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r3: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r4: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r5: `ceq < deviceB | ('key' : OldKey , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : OldKey , ..) > if OldKey =/= nils .`
- r6: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r7: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r8: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r9: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 778fa1250a42.json (run2, run3)

effect acc 77.8 rec 87.5; exact acc 77.8 rec 87.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  | exact |  |  |  |
| r2 |  |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  | exact |
| r4 | exact |  |  |  |  |  |  |  |
| r5 |  | exact |  |  |  |  |  |  |
| r6 |  |  | exact |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  | exact |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : nils , ..) > $ cloudA 'callAPI:openWindow' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , ..) > .`
- g2: `eq < DeviceX | ('key' : KeyA , 'trustSet' : SetA , ..) > $ UserX 'callAPI:bind' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'trustSet' : (SetA , UserX) , ..) > .`
- g3: `eq < DeviceX | ('on' : false , 'trustSet' : (SetA , PrincipalX) , ...) > $ PrincipalX 'callAPI:toggle' DeviceX = < DeviceX | ('on' : true , 'trustSet' : (SetA , PrincipalX) , ...) > .`
- g4: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ UserX 'cloudAPI:toggle' cloudA = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ cloudA 'callAPI:toggle' DeviceX .`
- g5: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g6: `eq < cloudA | (UserX : ('members' : (SetA , UserY) , 'device' : DeviceX , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : SetA , 'device' : DeviceX , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g7: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ UserX 'callAPI:openWindow' cloudA | (DeviceX) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('KeyA', N) , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ cloudA 'callAPI:openWindow' DeviceX | (randomStr('KeyA', N)) .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r3: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r4: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r5: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r6: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r8: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r9: `eq < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > .`

## cd7ac2ed3c7c.json (run4)

effect acc 77.8 rec 87.5; exact acc 77.8 rec 87.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  | exact |  |  |  |
| r2 |  |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  | exact |
| r4 | exact |  |  |  |  |  |  |  |
| r5 |  | exact |  |  |  |  |  |  |
| r6 |  |  | exact |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  | exact |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : nils , ..) > $ cloudA 'callAPI:openWindow' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , ..) > .`
- g2: `eq < DeviceX | ('key' : KeyA , 'trustSet' : SetA , ..) > $ UserX 'callAPI:bind' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'trustSet' : (SetA , UserX) , ..) > .`
- g3: `eq < DeviceX | ('on' : false , 'trustSet' : (SetA , PrincipalX) , ...) > $ PrincipalX 'callAPI:toggle' DeviceX = < DeviceX | ('on' : true , 'trustSet' : (SetA , PrincipalX) , ...) > .`
- g4: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ UserX 'cloudAPI:toggle' cloudA = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ cloudA 'callAPI:toggle' DeviceX .`
- g5: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g6: `eq < cloudA | (UserX : ('members' : (SetA , UserY) , 'device' : DeviceX , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : SetA , 'device' : DeviceX , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g7: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ UserX 'callAPI:openWindow' cloudA | (DeviceX) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('KeyA', N) , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ cloudA 'callAPI:openWindow' DeviceX | (randomStr('KeyA', N)) .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : deviceB , 'members' : (UserY , Members) , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r3: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < cloudA | (UserX : ('device' : deviceB , ....) , .....) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r4: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r5: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r6: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r8: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r9: `eq < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 122f04845f24.json (run5)

effect acc 77.8 rec 87.5; exact acc 77.8 rec 87.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  | exact |  |  |  |
| r2 |  |  |  |  |  |  | exact |  |
| r3 |  |  |  |  |  |  |  | exact |
| r4 | exact |  |  |  |  |  |  |  |
| r5 |  | exact |  |  |  |  |  |  |
| r6 |  |  | exact |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  | exact |  |  |

Gold rules:

- g1: `eq < DeviceX | ('key' : nils , ..) > $ cloudA 'callAPI:openWindow' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , ..) > .`
- g2: `eq < DeviceX | ('key' : KeyA , 'trustSet' : SetA , ..) > $ UserX 'callAPI:bind' DeviceX | (KeyA) = < DeviceX | ('key' : KeyA , 'trustSet' : (SetA , UserX) , ..) > .`
- g3: `eq < DeviceX | ('on' : false , 'trustSet' : (SetA , PrincipalX) , ...) > $ PrincipalX 'callAPI:toggle' DeviceX = < DeviceX | ('on' : true , 'trustSet' : (SetA , PrincipalX) , ...) > .`
- g4: `eq < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ UserX 'cloudAPI:toggle' cloudA = < cloudA | (UserX : ('device' : DeviceX , ..) , ...) > $ cloudA 'callAPI:toggle' DeviceX .`
- g5: `eq < cloudA | (UserX : ('members' : SetA , ..) , ...) > $ UserX 'callAPI:invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (SetA , UserY) , ..) , ...) > .`
- g6: `eq < cloudA | (UserX : ('members' : (SetA , UserY) , 'device' : DeviceX , ..) , UserY : ('device' : DeviceX , ...) , ....) > $ UserX 'callAPI:kick' cloudA | (UserY) = < cloudA | (UserX : ('members' : SetA , 'device' : DeviceX , ..) , UserY : ('device' : nils , ...) , ....) > .`
- g7: `eq < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : DeviceX , 'members' : (SetA , UserY) , ..) , UserY : ('device' : DeviceX , ...) , ....) > .`
- g8: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ UserX 'callAPI:openWindow' cloudA | (DeviceX) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('KeyA', N) , ...) > < cloudA | (UserX : ('device' : DeviceX , ....) , .....) > $ cloudA 'callAPI:openWindow' DeviceX | (randomStr('KeyA', N)) .`

Generated rules (names as generated):

- r1: `eq < cloudA | (UserX : ('members' : Members , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , ...) > .`
- r2: `eq < cloudA | (UserX : ('device' : Device , 'members' : (UserY , Members) , ..) , UserY : ('device' : nils , ...) , ....) > = < cloudA | (UserX : ('device' : Device , 'members' : (UserY , Members) , ..) , UserY : ('device' : Device , ...) , ....) > .`
- r3: `eq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < cloudA | (UserX : ('device' : Device , ....) , .....) > $ UserX 'openWindow' cloudA | (Device) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < cloudA | (UserX : ('device' : Device , ....) , .....) > $ cloudA 'openWindow' Device | (randomStr('Key', N)) .`
- r4: `eq < Device | ('key' : nils , ..) > $ cloudA 'openWindow' Device | (Key) = < Device | ('key' : Key , ..) > .`
- r5: `eq < Device | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' Device | (Key) = < Device | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r6: `eq < Device | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' Device = < Device | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('device' : Device , ..) , ...) > $ UserX 'turnOn' cloudA = < cloudA | (UserX : ('device' : Device , ..) , ...) > $ cloudA 'turnOn' Device .`
- r8: `eq < Device | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' Device = < Device | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r9: `eq < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : Device , ..) , UserY : ('device' : Device , ...) , ....) > $ UserX 'removeMember' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , 'device' : Device , ..) , UserY : ('device' : nils , ...) , ....) > .`

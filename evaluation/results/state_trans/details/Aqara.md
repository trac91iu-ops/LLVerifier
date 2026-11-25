# Aqara: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 0ff12f63734f.json (run1)

effect acc 70.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  |  | exact (gen wider) |
| r2 | exact |  |  |  |  |  |  |  |
| r3 |  | exact |  |  |  |  |  |  |
| r4 |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  | exact (gen narrower) |  |  |  |
| r9 |  |  |  |  | exact (gen narrower) |  |  |  |
| r10 |  |  |  |  |  | exact (gen wider) |  |  |

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

- r1: `eq < system | ('counter' : N , ..) > < UserX | ('key' : OldKey , ...) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r2: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r3: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r4: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r5: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r6: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r8: `eq < cloudA | (UserX : ('members' : Members , 'device' : nils , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : nils , ..) , UserY : ('device' : nils , ...) , ....) > .`
- r9: `ceq < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : AssociatedDevice , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : AssociatedDevice , ...) , ....) > if AssociatedDevice =/= nils .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : OldDevice , ...) , ....) > $ UserX 'remove' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : nils , ...) , ....) > .`

## cd5e0c5e2471.json (run2)

effect acc 70.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  |  | exact (gen wider) |
| r2 | exact |  |  |  |  |  |  |  |
| r3 |  | exact |  |  |  |  |  |  |
| r4 |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  | exact (gen narrower) |  |  |  |
| r9 |  |  |  |  | exact (gen narrower) |  |  |  |
| r10 |  |  |  |  |  | exact (gen wider) |  |  |

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

- r1: `eq < system | ('counter' : N , ..) > < UserX | ('key' : OldKey , ...) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r2: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r3: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r4: `eq < deviceB | ('trusted' : (UserX , Trusted) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Trusted) , 'on' : true , ..) > .`
- r5: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r6: `eq < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Trusted) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r8: `ceq < cloudA | (UserX : ('members' : Members , 'device' : AssociationX , ..) , UserY : ('device' : AssociationY , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : AssociationX , ..) , UserY : ('device' : AssociationY , ...) , ....) > if AssociationY =/= nils .`
- r9: `eq < cloudA | (UserX : ('members' : Members , 'device' : nils , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : nils , ..) , UserY : ('device' : nils , ...) , ....) > .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Members) , ..) , UserY : ('device' : OldDevice , ...) , ....) > $ UserX 'remove' cloudA | (UserY) = < cloudA | (UserX : ('members' : Members , ..) , UserY : ('device' : nils , ...) , ....) > .`

## e37da3d26094.json (run3)

effect acc 70.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  |  | exact (gen wider) |
| r2 | exact |  |  |  |  |  |  |  |
| r3 |  | exact |  |  |  |  |  |  |
| r4 |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  | exact (gen narrower) |  |  |  |
| r9 |  |  |  |  | exact (gen narrower) |  |  |  |
| r10 |  |  |  |  |  | exact (gen wider) |  |  |

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

- r1: `eq < system | ('counter' : N , ..) > < UserX | ('key' : OldKey , ...) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r2: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r3: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r4: `eq < deviceB | ('trusted' : (UserX , Rest) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Rest) , 'on' : true , ..) > .`
- r5: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r6: `eq < deviceB | ('trusted' : (cloudA , Rest) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Rest) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r8: `eq < cloudA | (UserX : ('members' : Members , 'device' : nils , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : nils , ..) , ...) > .`
- r9: `ceq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : AssociatedDevice , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : AssociatedDevice , ...) , ....) > if AssociatedDevice =/= nils .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : OldDevice , ...) , ....) > $ UserX 'remove' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## c576acadd367.json (run4)

effect acc 70.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  |  | exact (gen wider) |
| r2 | exact |  |  |  |  |  |  |  |
| r3 |  | exact |  |  |  |  |  |  |
| r4 |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  | exact (gen narrower) |  |  |  |
| r9 |  |  |  |  | exact (gen narrower) |  |  |  |
| r10 |  |  |  |  |  | exact (gen wider) |  |  |

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

- r1: `eq < system | ('counter' : N , ..) > < UserX | ('key' : OldKey , ...) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r2: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r3: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r4: `eq < deviceB | ('trusted' : (UserX , Rest) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Rest) , 'on' : true , ..) > .`
- r5: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r6: `eq < deviceB | ('trusted' : (cloudA , Rest) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Rest) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r8: `eq < cloudA | (UserX : ('members' : Members , 'device' : nils , ..) , UserY : ('device' : Association , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : nils , ..) , UserY : ('device' : Association , ...) , ....) > .`
- r9: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : DeviceY , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : DeviceY , ...) , ....) > .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : OldDevice , ...) , ....) > $ UserX 'remove' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

## 642e52196e45.json (run5)

effect acc 70.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  |  | exact (gen wider) |
| r2 | exact |  |  |  |  |  |  |  |
| r3 |  | exact |  |  |  |  |  |  |
| r4 |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  | exact (gen narrower) |  |  |  |
| r9 |  |  |  |  | exact (gen narrower) |  |  |  |
| r10 |  |  |  |  |  | exact (gen wider) |  |  |

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

- r1: `eq < system | ('counter' : N , ..) > < UserX | ('key' : OldKey , ...) > $ UserX 'openWindow' cloudA | (deviceB) = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > $ cloudA 'openWindow' deviceB | (randomStr('Key', N)) .`
- r2: `eq < deviceB | ('key' : nils , ..) > $ cloudA 'openWindow' deviceB | (Key) = < deviceB | ('key' : Key , ..) > .`
- r3: `eq < deviceB | ('key' : Key , 'trusted' : Trusted , ..) > $ UserX 'bind' deviceB | (Key) = < deviceB | ('key' : Key , 'trusted' : (UserX , Trusted) , ..) > .`
- r4: `eq < deviceB | ('trusted' : (UserX , Rest) , 'on' : false , ..) > $ UserX 'turnOn' deviceB = < deviceB | ('trusted' : (UserX , Rest) , 'on' : true , ..) > .`
- r5: `eq < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ UserX 'turnOn' cloudA | (deviceB) = < cloudA | (UserX : ('device' : deviceB , ..) , ...) > $ cloudA 'turnOn' deviceB .`
- r6: `eq < deviceB | ('trusted' : (cloudA , Rest) , 'on' : false , ..) > $ cloudA 'turnOn' deviceB = < deviceB | ('trusted' : (cloudA , Rest) , 'on' : true , ..) > .`
- r7: `eq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : nils , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : deviceB , ...) , ....) > .`
- r8: `eq < cloudA | (UserX : ('members' : Members , 'device' : nils , ..) , ...) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : nils , ..) , ...) > .`
- r9: `ceq < cloudA | (UserX : ('members' : Members , 'device' : deviceB , ..) , UserY : ('device' : Association , ...) , ....) > $ UserX 'invite' cloudA | (UserY) = < cloudA | (UserX : ('members' : (UserY , Members) , 'device' : deviceB , ..) , UserY : ('device' : Association , ...) , ....) > if Association =/= nils .`
- r10: `eq < cloudA | (UserX : ('members' : (UserY , Rest) , ..) , UserY : ('device' : OldDevice , ...) , ....) > $ UserX 'remove' cloudA | (UserY) = < cloudA | (UserX : ('members' : Rest , ..) , UserY : ('device' : nils , ...) , ....) > .`

# MaagKwikset: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 3ed990f917f8.json (run1, run5)

effect acc 75.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 | exact (gen narrower) |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  | exact |  |  |  |  |
| r8 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < system | ('counter' : N , ..) > < DeviceX | ('key' : KeyA , ...) > < UserY | ('key' : nils , ....) > $ UserY 'callAPI:getKey' DeviceX = < system | ('counter' : N + 1 , ..) > < DeviceX | ('key' : randomStr('KeyA', N) , ...) > < UserY | ('key' : randomStr('KeyA', N) , ....) > .`
- g2: `eq < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ UserY 'callAPI:signKey' cloudA | (DeviceX ; KeyA) = < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ cloudA 'send' UserY | (encrypt('secret', KeyA)) .`
- g3: `eq < DeviceX | ('key' : KeyA , 'trust' : SetA , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > $ UserY 'callAPI:bind' DeviceX | (encrypt('secret', KeyA)) = < DeviceX | ('key' : KeyA , 'trust' : (SetA , UserY) , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > .`
- g4: `eq < cloudA | (DeviceX : ('trust' : SetA , ..) , ...) > $ UserX 'callAPI:share' cloudA | (UserY ; DeviceX) = < cloudA | (DeviceX : ('trust' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (DeviceX : ('trust' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' cloudA | (UserY) = < cloudA | (DeviceX : ('trust' : (UserX , ..) , ...) , ....) > .`
- g6: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'send' UserX | (SignedKeyA) = < UserX | ('signedKey' : SignedKeyA , ..) > .`
- g7: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g8: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `ceq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < deviceB | ('key' : Key , ....) > $ UserX 'requestKey' deviceB = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < deviceB | ('key' : randomStr('Key', N) , ....) > if Key =/= nils .`
- r4: `eq < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'signKey' cloudA | (deviceB ; Key) = < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ cloudA 'signedKey' UserX | (deviceB ; encrypt(Key, Secret)) .`
- r5: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'signedKey' UserX | (deviceB ; SignedKey) = < UserX | ('signedKey' : SignedKey , ..) > .`
- r6: `eq < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : Trusted , ...) > $ UserX 'bind' deviceB | (encrypt(Key, Secret)) = < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : (UserX , Trusted) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('trusted' : Trusted , ..) , ...) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserY , Trusted) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > .`

## 5293f1bc4013.json (run2)

effect acc 75.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 | exact (gen narrower) |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  | exact |  |  |  |  |
| r8 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < system | ('counter' : N , ..) > < DeviceX | ('key' : KeyA , ...) > < UserY | ('key' : nils , ....) > $ UserY 'callAPI:getKey' DeviceX = < system | ('counter' : N + 1 , ..) > < DeviceX | ('key' : randomStr('KeyA', N) , ...) > < UserY | ('key' : randomStr('KeyA', N) , ....) > .`
- g2: `eq < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ UserY 'callAPI:signKey' cloudA | (DeviceX ; KeyA) = < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ cloudA 'send' UserY | (encrypt('secret', KeyA)) .`
- g3: `eq < DeviceX | ('key' : KeyA , 'trust' : SetA , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > $ UserY 'callAPI:bind' DeviceX | (encrypt('secret', KeyA)) = < DeviceX | ('key' : KeyA , 'trust' : (SetA , UserY) , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > .`
- g4: `eq < cloudA | (DeviceX : ('trust' : SetA , ..) , ...) > $ UserX 'callAPI:share' cloudA | (UserY ; DeviceX) = < cloudA | (DeviceX : ('trust' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (DeviceX : ('trust' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' cloudA | (UserY) = < cloudA | (DeviceX : ('trust' : (UserX , ..) , ...) , ....) > .`
- g6: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'send' UserX | (SignedKeyA) = < UserX | ('signedKey' : SignedKeyA , ..) > .`
- g7: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g8: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `ceq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < deviceB | ('key' : Key , ....) > $ UserX 'requestKey' deviceB = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < deviceB | ('key' : randomStr('Key', N) , ....) > if Key =/= nils .`
- r4: `eq < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'signKey' cloudA | (deviceB ; Key) = < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ cloudA 'signedKey' UserX | (deviceB ; encrypt(Key, Secret)) .`
- r5: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'signedKey' UserX | (deviceB ; SignedKey) = < UserX | ('signedKey' : SignedKey , ..) > .`
- r6: `eq < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : Trusted , ...) > $ UserX 'bind' deviceB | (encrypt(Key, Secret)) = < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : (UserX , Trusted) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('trusted' : Trusted , ..) , ...) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserY , Trusted) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > .`

## 5785c25ea698.json (run3)

effect acc 75.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 | exact (gen narrower) |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  | exact |  |  |  |  |
| r8 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < system | ('counter' : N , ..) > < DeviceX | ('key' : KeyA , ...) > < UserY | ('key' : nils , ....) > $ UserY 'callAPI:getKey' DeviceX = < system | ('counter' : N + 1 , ..) > < DeviceX | ('key' : randomStr('KeyA', N) , ...) > < UserY | ('key' : randomStr('KeyA', N) , ....) > .`
- g2: `eq < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ UserY 'callAPI:signKey' cloudA | (DeviceX ; KeyA) = < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ cloudA 'send' UserY | (encrypt('secret', KeyA)) .`
- g3: `eq < DeviceX | ('key' : KeyA , 'trust' : SetA , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > $ UserY 'callAPI:bind' DeviceX | (encrypt('secret', KeyA)) = < DeviceX | ('key' : KeyA , 'trust' : (SetA , UserY) , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > .`
- g4: `eq < cloudA | (DeviceX : ('trust' : SetA , ..) , ...) > $ UserX 'callAPI:share' cloudA | (UserY ; DeviceX) = < cloudA | (DeviceX : ('trust' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (DeviceX : ('trust' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' cloudA | (UserY) = < cloudA | (DeviceX : ('trust' : (UserX , ..) , ...) , ....) > .`
- g6: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'send' UserX | (SignedKeyA) = < UserX | ('signedKey' : SignedKeyA , ..) > .`
- g7: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g8: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `ceq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < deviceB | ('key' : Key , ....) > $ UserX 'requestKey' deviceB = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < deviceB | ('key' : randomStr('Key', N) , ....) > if Key =/= nils .`
- r4: `eq < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'signKey' cloudA | (deviceB ; Key) = < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ cloudA 'sendSignedKey' UserX | (deviceB ; encrypt(Key, Secret)) .`
- r5: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'sendSignedKey' UserX | (deviceB ; SignedKey) = < UserX | ('signedKey' : SignedKey , ..) > .`
- r6: `eq < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : Trusted , ...) > $ UserX 'bind' deviceB | (encrypt(Key, Secret)) = < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : (UserX , Trusted) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('trusted' : Trusted , ..) , ...) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserY , Trusted) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > .`

## b23685b06634.json (run4)

effect acc 75.0 rec 75.0; exact acc 50.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 | exact (gen narrower) |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  | exact |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  | exact |  |  |  |  |
| r8 |  |  |  |  | exact |  |  |  |

Gold rules:

- g1: `eq < system | ('counter' : N , ..) > < DeviceX | ('key' : KeyA , ...) > < UserY | ('key' : nils , ....) > $ UserY 'callAPI:getKey' DeviceX = < system | ('counter' : N + 1 , ..) > < DeviceX | ('key' : randomStr('KeyA', N) , ...) > < UserY | ('key' : randomStr('KeyA', N) , ....) > .`
- g2: `eq < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ UserY 'callAPI:signKey' cloudA | (DeviceX ; KeyA) = < cloudA | (DeviceX : ('trust' : (UserY , ..) , ...) , ....) > $ cloudA 'send' UserY | (encrypt('secret', KeyA)) .`
- g3: `eq < DeviceX | ('key' : KeyA , 'trust' : SetA , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > $ UserY 'callAPI:bind' DeviceX | (encrypt('secret', KeyA)) = < DeviceX | ('key' : KeyA , 'trust' : (SetA , UserY) , ..) > < UserY | ('signedKey' : encrypt('secret', KeyA) , ...) > .`
- g4: `eq < cloudA | (DeviceX : ('trust' : SetA , ..) , ...) > $ UserX 'callAPI:share' cloudA | (UserY ; DeviceX) = < cloudA | (DeviceX : ('trust' : (SetA , UserY) , ..) , ...) > .`
- g5: `eq < cloudA | (DeviceX : ('trust' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' cloudA | (UserY) = < cloudA | (DeviceX : ('trust' : (UserX , ..) , ...) , ....) > .`
- g6: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'send' UserX | (SignedKeyA) = < UserX | ('signedKey' : SignedKeyA , ..) > .`
- g7: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g8: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `ceq < system | ('counter' : N , ..) > < UserX | ('key' : nils , ...) > < deviceB | ('key' : DeviceKey , ....) > $ UserX 'requestKey' deviceB = < system | ('counter' : N + 1 , ..) > < UserX | ('key' : randomStr('Key', N) , ...) > < deviceB | ('key' : randomStr('Key', N) , ....) > if DeviceKey =/= nils .`
- r4: `eq < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'signKey' cloudA | (deviceB ; Key) = < cloudA | ('secret' : Secret , deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > $ cloudA 'signedKey' UserX | (deviceB ; encrypt(Key, Secret)) .`
- r5: `eq < UserX | ('signedKey' : nils , ..) > $ cloudA 'signedKey' UserX | (deviceB ; SignedKey) = < UserX | ('signedKey' : SignedKey , ..) > .`
- r6: `eq < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : Trusted , ...) > $ UserX 'bind' deviceB | (encrypt(Key, Secret)) = < UserX | ('signedKey' : encrypt(Key, Secret) , ..) > < deviceB | ('key' : Key , 'secret' : Secret , 'trusted' : (UserX , Trusted) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('trusted' : Trusted , ..) , ...) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserY , Trusted) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | (deviceB : ('trusted' : (UserX , Rest) , ..) , ...) > .`

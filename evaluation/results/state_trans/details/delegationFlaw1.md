# delegationFlaw1: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 8f347a200ea2.json (run1)

effect acc 75.0 rec 75.0; exact acc 75.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  | exact (gen narrower) |  |  |  |  |
| r2 |  |  |  |  | exact |  |  |  |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  | exact |
| r6 |  | exact |  |  |  |  |  |  |
| r7 |  |  | exact |  |  |  |  |  |
| r8 | exact |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'send' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('trust' : (....), 'key' : KeyA , ..) , ...) > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('trust' : (PrincipalX , ....) , 'key' : KeyA , ..) , ...) > .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trusted' : (UserX , Trusted) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trusted' : (UserX , Trusted) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trusted' : (UserX , Trusted) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Trusted) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Trusted) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , Trusted) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : Trusted , ..) , ...) > $ UserX 'provideKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : (UserX , Trusted) , ..) , ...) > .`
- r6: `eq < CloudX | (DeviceX : ('on' : false , 'trusted' : (P , Trusted) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trusted' : (P , Trusted) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r7: `eq < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r8: `eq < deviceLock | ('trusted' : (P , Trusted) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Trusted) , 'on' : true , ..) > .`

## f10a7852d86d.json (run2)

effect acc 75.0 rec 75.0; exact acc 75.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  | exact (gen narrower) |  |  |  |  |
| r2 |  |  |  |  | exact |  |  |  |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  | exact |
| r6 |  | exact |  |  |  |  |  |  |
| r7 |  |  | exact |  |  |  |  |  |
| r8 | exact |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'send' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('trust' : (....), 'key' : KeyA , ..) , ...) > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('trust' : (PrincipalX , ....) , 'key' : KeyA , ..) , ...) > .`

Generated rules (names as generated):

- r1: `ceq < Cloud | (Device : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' Cloud = < Cloud | (Device : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ Cloud 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ Cloud 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < Cloud | (Device : ('trust' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trust' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < Cloud | (Device : ('trust' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trust' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (Device : ('key' : Key , 'trust' : Trusted , ..) , ...) > $ UserX 'provideKey' cloudSmartThing | (Device ; Key) = < cloudSmartThing | (Device : ('key' : Key , 'trust' : (UserX , Trusted) , ..) , ...) > .`
- r6: `eq < Cloud | (Device : ('on' : false , 'trust' : (P , Rest) , ..) , ...) > $ P 'turnOn' Device = < Cloud | (Device : ('on' : true , 'trust' : (P , Rest) , ..) , ...) > $ Cloud 'turnOn' Device .`
- r7: `eq < cloudSmartThing | (Device : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' Device = < cloudSmartThing | (Device : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r8: `eq < deviceLock | ('trust' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trust' : (P , Rest) , 'on' : true , ..) > .`

## 3dd3d60f0dba.json (a2-run1)

effect acc 66.7 rec 75.0; exact acc 66.7 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  | exact (gen narrower) |  |  |  |  |
| r2 |  |  |  |  | exact |  |  |  |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  | exact |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  | exact |  |  |  |  |  |  |
| r8 |  |  | exact |  |  |  |  |  |
| r9 | exact |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'send' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('trust' : (....), 'key' : KeyA , ..) , ...) > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('trust' : (PrincipalX , ....) , 'key' : KeyA , ..) , ...) > .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : Trusted , ..) , ...) > $ UserX 'provideKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : (UserX , Trusted) , ..) , ...) > .`
- r6: `eq < DeviceX | (..) > $ UserX 'turnOn' DeviceX = < DeviceX | (..) > .`
- r7: `eq < CloudX | (DeviceX : ('on' : false , 'trusted' : (P , Rest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trusted' : (P , Rest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r8: `eq < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trusted' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Rest) , 'on' : true , ..) > .`

## 8363f3ffc221.json (run4)

effect acc 66.7 rec 75.0; exact acc 66.7 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  | exact (gen narrower) |  |  |  |  |
| r2 |  |  |  |  | exact |  |  |  |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  | exact |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  | exact |  |  |  |  |  |  |
| r8 |  |  | exact |  |  |  |  |  |
| r9 | exact |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'send' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('trust' : (....), 'key' : KeyA , ..) , ...) > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('trust' : (PrincipalX , ....) , 'key' : KeyA , ..) , ...) > .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trusted' : (UserX , TrustedRest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trusted' : (UserX , TrustedRest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trusted' : (UserX , TrustedRest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , UserY , TrustedRest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trusted' : (UserX , UserY , TrustedRest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , TrustedRest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : Trusted , ..) , ...) > $ UserX 'provideKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : (UserX , Trusted) , ..) , ...) > .`
- r6: `eq < DeviceX | (..) > $ UserX 'turnOn' DeviceX = < DeviceX | (..) > .`
- r7: `eq < CloudX | (DeviceX : ('on' : false , 'trusted' : (P , TrustedRest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trusted' : (P , TrustedRest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r8: `eq < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trusted' : (P , TrustedRest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , TrustedRest) , 'on' : true , ..) > .`

## c15d79fe7faa.json (run3)

effect acc 75.0 rec 75.0; exact acc 75.0 rec 62.5

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  | exact (gen narrower) |  |  |  |  |
| r2 |  |  |  |  | exact |  |  |  |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  |  |  |  | exact |
| r6 |  | exact |  |  |  |  |  |  |
| r7 |  |  | exact |  |  |  |  |  |
| r8 | exact |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trust' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trust' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trust' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'send' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'send' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trust' : (UserX , UserZ , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trust' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('trust' : (....), 'key' : KeyA , ..) , ...) > $ PrincipalX 'callAPI:provide' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('trust' : (PrincipalX , ....) , 'key' : KeyA , ..) , ...) > .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : Trusted , ..) , ...) > $ UserX 'provideKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'trusted' : (UserX , Trusted) , ..) , ...) > .`
- r6: `eq < CloudX | (DeviceX : ('on' : false , 'trusted' : (P , Rest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trusted' : (P , Rest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r7: `eq < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r8: `eq < deviceLock | ('trusted' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Rest) , 'on' : true , ..) > .`

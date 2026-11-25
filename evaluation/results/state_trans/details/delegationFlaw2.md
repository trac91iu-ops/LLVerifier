# delegationFlaw2: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## e59434542390.json (run1)

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

- g1: `eq < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'sendKey' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserY ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : false , ..) , ...) > $ UserX 'callAPI:cloudAPI:toggle' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : true , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trusted' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : false , ..) , ...) > $ UserX 'turnOnWithKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : true , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX .`
- r6: `eq < DeviceX | (..) > $ UserX 'turnOn' DeviceX = < DeviceX | (..) > .`
- r7: `eq < CloudX | (DeviceX : ('on' : false , 'trusted' : (P , Rest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trusted' : (P , Rest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r8: `eq < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trusted' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Rest) , 'on' : true , ..) > .`

## 57863c610aa9.json (run3)

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

- g1: `eq < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'sendKey' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserY ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : false , ..) , ...) > $ UserX 'callAPI:cloudAPI:toggle' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : true , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trust' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trust' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trust' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trust' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : false , ..) , ...) > $ UserX 'turnOnWithKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : true , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX .`
- r6: `eq < DeviceX | (..) > $ UserX 'turnOn' DeviceX = < DeviceX | (..) > .`
- r7: `eq < CloudX | (DeviceX : ('on' : false , 'trust' : (P , Rest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trust' : (P , Rest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r8: `eq < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trust' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trust' : (P , Rest) , 'on' : true , ..) > .`

## e4dd9de0ea5d.json (run3)

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

- g1: `eq < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'sendKey' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserY ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : false , ..) , ...) > $ UserX 'callAPI:cloudAPI:toggle' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : true , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX .`

Generated rules (names as generated):

- r1: `ceq < Cloud | (Device : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' Cloud = < Cloud | (Device : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ Cloud 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ Cloud 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < Cloud | (Device : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < Cloud | (Device : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trusted' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (Device : ('key' : Key , 'on' : false , ..) , ...) > $ UserX 'turnOnWithKey' cloudSmartThing | (Device ; Key) = < cloudSmartThing | (Device : ('key' : Key , 'on' : true , ..) , ...) > $ cloudSmartThing 'turnOn' Device .`
- r6: `eq < Device | (..) > $ UserX 'turnOn' Device = < Device | (..) > .`
- r7: `eq < Cloud | (Device : ('on' : false , 'trusted' : (P , Rest) , ..) , ...) > $ P 'turnOn' Device = < Cloud | (Device : ('on' : true , 'trusted' : (P , Rest) , ..) , ...) > $ Cloud 'turnOn' Device .`
- r8: `eq < cloudSmartThing | (Device : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' Device = < cloudSmartThing | (Device : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trusted' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Rest) , 'on' : true , ..) > .`

## 50e6ccdc853b.json (run4)

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

- g1: `eq < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'sendKey' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserY ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : false , ..) , ...) > $ UserX 'callAPI:cloudAPI:toggle' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : true , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX .`

Generated rules (names as generated):

- r1: `ceq < CloudX | (DeviceX : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' CloudX = < CloudX | (DeviceX : ('trust' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ CloudX 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < CloudX | (DeviceX : ('trust' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trust' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < CloudX | (DeviceX : ('trust' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' CloudX | (DeviceX ; UserY) = < CloudX | (DeviceX : ('trust' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : false , ..) , ...) > $ UserX 'turnOnWithKey' cloudSmartThing | (DeviceX ; Key) = < cloudSmartThing | (DeviceX : ('key' : Key , 'on' : true , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX .`
- r6: `eq < DeviceX | (..) > $ UserX 'turnOn' DeviceX = < DeviceX | (..) > .`
- r7: `eq < CloudX | (DeviceX : ('on' : false , 'trust' : (P , Rest) , ..) , ...) > $ P 'turnOn' DeviceX = < CloudX | (DeviceX : ('on' : true , 'trust' : (P , Rest) , ..) , ...) > $ CloudX 'turnOn' DeviceX .`
- r8: `eq < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' DeviceX = < cloudSmartThing | (DeviceX : ('bound' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r9: `eq < deviceLock | ('trust' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trust' : (P , Rest) , 'on' : true , ..) > .`

## dd32e24657be.json (run5)

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

- g1: `eq < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) > $ PrincipalX 'callAPI:toggle' deviceLock = < deviceLock | ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) > .`
- g2: `eq < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : false , ...) , ....) > $ PrincipalX 'callAPI:toggle' DeviceY = < CloudX | (DeviceY : ('trustSet' : (PrincipalX , ..) , 'state' : true , ...) , ....) > $ CloudX 'callAPI:toggle' DeviceY .`
- g3: `eq < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX = < cloudSmartThing | (DeviceX : ('boundTo' : DeviceY , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceY .`
- g4: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ UserX 'callAPI:getKey' CloudX = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , 'key' : KeyA , ...) , ....) > $ CloudX 'sendKey' UserX | (KeyA) .`
- g5: `eq < UserX | ('key' : nils , ..) > $ CloudX 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g6: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > $ UserX 'callAPI:delegate' CloudX | (UserZ ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , UserZ , ..) , ...) , ....) > .`
- g7: `eq < CloudX | (DeviceY : ('trustSet' : (UserX , UserY , ..) , ...) , ....) > $ UserX 'callAPI:revoke' CloudX | (UserY ; DeviceY) = < CloudX | (DeviceY : ('trustSet' : (UserX , ..) , ...) , ....) > .`
- g8: `eq < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : false , ..) , ...) > $ UserX 'callAPI:cloudAPI:toggle' cloudSmartThing | (DeviceX ; KeyA) = < cloudSmartThing | (DeviceX : ('key' : KeyA , 'state' : true , ..) , ...) > $ cloudSmartThing 'callAPI:toggle' DeviceX .`

Generated rules (names as generated):

- r1: `ceq < Cloud | (Device : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ UserX 'requestKey' Cloud = < Cloud | (Device : ('trusted' : (UserX , Rest) , 'key' : Key , ..) , ...) > $ Cloud 'sendKey' UserX | (Key) if Key =/= nils .`
- r2: `eq < UserX | ('key' : nils , ..) > $ Cloud 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r3: `eq < Cloud | (Device : ('trusted' : (UserX , Rest) , ..) , ...) > $ UserX 'delegateAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > .`
- r4: `eq < Cloud | (Device : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > $ UserX 'revokeAccess' Cloud | (Device ; UserY) = < Cloud | (Device : ('trusted' : (UserX , Rest) , ..) , ...) > .`
- r5: `eq < cloudSmartThing | (Device : ('key' : Key , 'on' : false , ..) , ...) > $ UserX 'turnOnWithKey' cloudSmartThing | (Device ; Key) = < cloudSmartThing | (Device : ('key' : Key , 'on' : true , ..) , ...) > $ cloudSmartThing 'turnOn' Device .`
- r6: `eq < Cloud | (Device : ('on' : false , 'trusted' : (P , Rest) , ..) , ...) > $ P 'turnOn' Device = < Cloud | (Device : ('on' : true , 'trusted' : (P , Rest) , ..) , ...) > $ Cloud 'turnOn' Device .`
- r7: `eq < cloudSmartThing | (Device : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' Device = < cloudSmartThing | (Device : ('boundTo' : B , ..) , ...) > $ cloudSmartThing 'turnOn' B .`
- r8: `eq < deviceLock | ('trusted' : (P , Rest) , 'on' : false , ..) > $ P 'turnOn' deviceLock = < deviceLock | ('trusted' : (P , Rest) , 'on' : true , ..) > .`

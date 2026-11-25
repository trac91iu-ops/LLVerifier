# MaagLevel: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## b510c989c0bd.json (run1)

effect acc 33.3 rec 37.5; exact acc 0.0 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ...) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ UserA 'callAPI:revoke' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'revoke' ; UserB) .`
- g2: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ UserA 'callAPI:share' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ..) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'share' ; UserB) .`
- g3: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'share' ; UserB) < DeviceX | ('trustSet' : (...) , ....) > = < DeviceX | ('trustSet' : (UserB , ...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g4: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'revoke' ; UserB) < DeviceX | ('trustSet' : (UserB , ...) , ....) > = < DeviceX | ('trustSet' : (...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g5: `eq < userA | ('localTo' : DeviceX , ...) > $ cloudA 'send' UserA | (DeviceX ; CommandList) = < userA | ('localTo' : DeviceX , ...) > $ UserA 'callAPI:proxy' DeviceX | (CommandList) .`
- g6: `eq < userC | ('localTo' : DeviceX , 'commandList' : nils , ...) > $ cloudA 'send' UserC | (DeviceX ; CommandList) = < userC | ('localTo' : DeviceX , 'commandList' : list(CommandList) , ...) > .`
- g7: `eq < UserA | ('localTo' : nils , ..) > $ UserA 'approaches' DeviceX = < UserA | ('localTo' : DeviceX , ..) > .`
- g8: `eq < UserA | ('localTo' : DeviceX , ..) > $ UserA 'leaves' DeviceX = < UserA | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , ..) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'share' ; UserY))) .`
- r4: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) .`
- r5: `eq < ImmediateRelayUser | ('near' : deviceB , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < ImmediateRelayUser | ('near' : deviceB , ..) > $ RelayUser 'forwardCommand' deviceB | (L) .`
- r6: `eq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > .`
- r7: `ceq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ CachingRelayUser 'forwardCommand' deviceB | (L) if L =/= nils .`
- r8: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Trusted , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'share' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Trusted) , ...) > .`
- r9: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Rest) , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Rest , ...) > .`

## b3a871fff63f.json (run2)

effect acc 33.3 rec 37.5; exact acc 22.2 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact |  |
| r2 |  |  |  |  |  |  |  | exact |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ...) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ UserA 'callAPI:revoke' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'revoke' ; UserB) .`
- g2: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ UserA 'callAPI:share' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ..) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'share' ; UserB) .`
- g3: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'share' ; UserB) < DeviceX | ('trustSet' : (...) , ....) > = < DeviceX | ('trustSet' : (UserB , ...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g4: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'revoke' ; UserB) < DeviceX | ('trustSet' : (UserB , ...) , ....) > = < DeviceX | ('trustSet' : (...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g5: `eq < userA | ('localTo' : DeviceX , ...) > $ cloudA 'send' UserA | (DeviceX ; CommandList) = < userA | ('localTo' : DeviceX , ...) > $ UserA 'callAPI:proxy' DeviceX | (CommandList) .`
- g6: `eq < userC | ('localTo' : DeviceX , 'commandList' : nils , ...) > $ cloudA 'send' UserC | (DeviceX ; CommandList) = < userC | ('localTo' : DeviceX , 'commandList' : list(CommandList) , ...) > .`
- g7: `eq < UserA | ('localTo' : nils , ..) > $ UserA 'approaches' DeviceX = < UserA | ('localTo' : DeviceX , ..) > .`
- g8: `eq < UserA | ('localTo' : DeviceX , ..) > $ UserA 'leaves' DeviceX = < UserA | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : nils , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : deviceB , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , ..) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'share' ; UserY))) .`
- r4: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) .`
- r5: `eq < ImmediateRelayUser | ('near' : deviceB , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < ImmediateRelayUser | ('near' : deviceB , ..) > $ RelayUser 'forwardCommand' deviceB | (L) .`
- r6: `eq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > .`
- r7: `ceq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ CachingRelayUser 'forwardCommand' deviceB | (L) if L =/= nils .`
- r8: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Trusted , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'share' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Trusted) , ...) > .`
- r9: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Rest) , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Rest , ...) > .`

## 69d01d2b7c77.json (run3)

effect acc 33.3 rec 37.5; exact acc 0.0 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ...) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ UserA 'callAPI:revoke' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'revoke' ; UserB) .`
- g2: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ UserA 'callAPI:share' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ..) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'share' ; UserB) .`
- g3: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'share' ; UserB) < DeviceX | ('trustSet' : (...) , ....) > = < DeviceX | ('trustSet' : (UserB , ...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g4: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'revoke' ; UserB) < DeviceX | ('trustSet' : (UserB , ...) , ....) > = < DeviceX | ('trustSet' : (...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g5: `eq < userA | ('localTo' : DeviceX , ...) > $ cloudA 'send' UserA | (DeviceX ; CommandList) = < userA | ('localTo' : DeviceX , ...) > $ UserA 'callAPI:proxy' DeviceX | (CommandList) .`
- g6: `eq < userC | ('localTo' : DeviceX , 'commandList' : nils , ...) > $ cloudA 'send' UserC | (DeviceX ; CommandList) = < userC | ('localTo' : DeviceX , 'commandList' : list(CommandList) , ...) > .`
- g7: `eq < UserA | ('localTo' : nils , ..) > $ UserA 'approaches' DeviceX = < UserA | ('localTo' : DeviceX , ..) > .`
- g8: `eq < UserA | ('localTo' : DeviceX , ..) > $ UserA 'leaves' DeviceX = < UserA | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , ..) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'share' ; UserY))) .`
- r4: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) .`
- r5: `eq < ImmediateRelayUser | ('near' : deviceB , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < ImmediateRelayUser | ('near' : deviceB , ..) > $ RelayUser 'forwardCommand' deviceB | (L) .`
- r6: `eq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > .`
- r7: `ceq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ CachingRelayUser 'forwardCommand' deviceB | (L) if L =/= nils .`
- r8: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Trusted , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'share' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Trusted) , ...) > .`
- r9: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Rest) , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Rest , ...) > .`

## 3dc0b0706da3.json (run4)

effect acc 33.3 rec 37.5; exact acc 0.0 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ...) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ UserA 'callAPI:revoke' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'revoke' ; UserB) .`
- g2: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ UserA 'callAPI:share' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ..) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'share' ; UserB) .`
- g3: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'share' ; UserB) < DeviceX | ('trustSet' : (...) , ....) > = < DeviceX | ('trustSet' : (UserB , ...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g4: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'revoke' ; UserB) < DeviceX | ('trustSet' : (UserB , ...) , ....) > = < DeviceX | ('trustSet' : (...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g5: `eq < userA | ('localTo' : DeviceX , ...) > $ cloudA 'send' UserA | (DeviceX ; CommandList) = < userA | ('localTo' : DeviceX , ...) > $ UserA 'callAPI:proxy' DeviceX | (CommandList) .`
- g6: `eq < userC | ('localTo' : DeviceX , 'commandList' : nils , ...) > $ cloudA 'send' UserC | (DeviceX ; CommandList) = < userC | ('localTo' : DeviceX , 'commandList' : list(CommandList) , ...) > .`
- g7: `eq < UserA | ('localTo' : nils , ..) > $ UserA 'approaches' DeviceX = < UserA | ('localTo' : DeviceX , ..) > .`
- g8: `eq < UserA | ('localTo' : DeviceX , ..) > $ UserA 'leaves' DeviceX = < UserA | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < UserRelay | ('near' : deviceB , ....) > $ UserX 'shareAccess' cloudA | (UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , ..) , ..) , ...) > < UserRelay | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' UserRelay | (deviceB ; list((encrypt('auth', 'secret') ; 'share' ; UserY))) .`
- r4: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > < UserRelay | ('near' : deviceB , ....) > $ UserX 'revokeAccess' cloudA | (UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < UserRelay | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' UserRelay | (deviceB ; list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) .`
- r5: `eq < UserImmediateRelay | ('near' : deviceB , ..) > $ cloudA 'deliverCommand' UserRelay | (deviceB ; L) = < UserImmediateRelay | ('near' : deviceB , ..) > $ UserRelay 'forwardCommand' deviceB | (L) .`
- r6: `eq < UserCachingRelay | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ cloudA 'deliverCommand' UserRelay | (deviceB ; L) = < UserCachingRelay | ('near' : deviceB , 'cachedCommand' : L , ..) > .`
- r7: `ceq < UserCachingRelay | ('near' : deviceB , 'cachedCommand' : L , ..) > = < UserCachingRelay | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ UserCachingRelay 'forwardCommand' deviceB | (L) if L =/= nils .`
- r8: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Trusted , ...) > $ UserRelay 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'share' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Trusted) , ...) > .`
- r9: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Rest) , ...) > $ UserRelay 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Rest , ...) > .`

## ddf75298815d.json (run3, run4)

effect acc 33.3 rec 37.5; exact acc 0.0 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 |
|---|---|---|---|---|---|---|---|---|
| r1 |  |  |  |  |  |  | exact (gen wider) |  |
| r2 |  |  |  |  |  |  |  | exact (gen wider) |
| r3 |  |  |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |
| r6 |  |  |  |  |  |  |  |  |
| r7 |  |  |  |  |  |  |  |  |
| r8 |  |  |  |  |  |  |  |  |
| r9 |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ...) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ UserA 'callAPI:revoke' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ....) , .....) > < UserC | ('localTo' : DeviceX , ......) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'revoke' ; UserB) .`
- g2: `eq < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ UserA 'callAPI:share' cloudA | (UserB) = < cloudA | ('cloudKey' : 'secret' , DeviceX : ('trustSet' : (UserA , UserB , ..) , ..) , ...) > < UserC | ('localTo' : DeviceX , ....) > $ cloudA 'send' UserC | (DeviceX ; encrypt('secret', 'auth') ; 'share' ; UserB) .`
- g3: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'share' ; UserB) < DeviceX | ('trustSet' : (...) , ....) > = < DeviceX | ('trustSet' : (UserB , ...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g4: `eq < cloudA | ('cloudKey' : 'secret' , ..) > $ UserA 'callAPI:proxy' DeviceX | (encrypt('secret', 'auth') ; 'revoke' ; UserB) < DeviceX | ('trustSet' : (UserB , ...) , ....) > = < DeviceX | ('trustSet' : (...) , ....) > < cloudA | ('cloudKey' : 'secret' , ..) > .`
- g5: `eq < userA | ('localTo' : DeviceX , ...) > $ cloudA 'send' UserA | (DeviceX ; CommandList) = < userA | ('localTo' : DeviceX , ...) > $ UserA 'callAPI:proxy' DeviceX | (CommandList) .`
- g6: `eq < userC | ('localTo' : DeviceX , 'commandList' : nils , ...) > $ cloudA 'send' UserC | (DeviceX ; CommandList) = < userC | ('localTo' : DeviceX , 'commandList' : list(CommandList) , ...) > .`
- g7: `eq < UserA | ('localTo' : nils , ..) > $ UserA 'approaches' DeviceX = < UserA | ('localTo' : DeviceX , ..) > .`
- g8: `eq < UserA | ('localTo' : DeviceX , ..) > $ UserA 'leaves' DeviceX = < UserA | ('localTo' : nils , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'shareAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , ..) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'share' ; UserY))) .`
- r4: `eq < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX , UserY , Rest) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ UserX 'revokeAccess' cloudA | (deviceB ; UserY) = < cloudA | ('key' : 'secret' , deviceB : ('trusted' : (UserX) , ..) , ...) > < RelayUser | ('near' : deviceB , ....) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) .`
- r5: `eq < ImmediateRelayUser | ('near' : deviceB , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < ImmediateRelayUser | ('near' : deviceB , ..) > $ RelayUser 'forwardCommand' deviceB | (L) .`
- r6: `eq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ cloudA 'deliverCommand' RelayUser | (deviceB ; L) = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > .`
- r7: `ceq < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : L , ..) > = < CachingRelayUser | ('near' : deviceB , 'cachedCommand' : nils , ..) > $ CachingRelayUser 'forwardCommand' deviceB | (L) if L =/= nils .`
- r8: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Trusted , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'share' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Trusted) , ...) > .`
- r9: `eq < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : (UserY , Rest) , ...) > $ RelayUser 'forwardCommand' deviceB | (list((encrypt('auth', 'secret') ; 'revoke' ; UserY))) = < cloudA | ('key' : 'secret' , ..) > < deviceB | ('trusted' : Rest , ...) > .`

# philips: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## f8e46debb859.json (run1)

effect acc 100.0 rec 100.0; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  | exact |  |  |  |
| r8 |  |  |  |  |  |  | effect |  |  |
| r9 |  |  |  |  |  |  |  | effect |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | (...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | (...) > $ DeviceY 'callAPI:setKey' cloudA | (randomStr('Secret', N)) .`
- g4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : SetX , ...) , ....) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (SetX , ('key' : KeyA , 'time' : CurrentTime)) , ...) , ....) > .`
- g5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ UserX 'callAPI:getKey' cloudA | (DeviceY) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ cloudA 'send' UserX | (KeyA) if CurrentTime < TimeA + 1 .`
- g6: `eq < cloudA | (DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g7: `eq < cloudA | (DeviceY : ('owner' : SetX , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (SetX , UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g8: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : nils , ....) , .....) > if CurrentTime > TimeA + 2 .`
- g9: `eq < UserX | ('knowledge' : SetX , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('knowledge' : (SetX , KeyA) , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | (...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | (...) > $ deviceB 'uploadSecret' cloudA | (deviceB ; randomStr('Secret', N)) .`
- r4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : Tickets , ...) , ....) > $ deviceB 'uploadSecret' cloudA | (deviceB ; Secret) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : CurrentTime) , Tickets) , ...) , ....) > .`
- r5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ UserX 'getKey' cloudA | (deviceB) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) if IssuedTime == CurrentTime .`
- r6: `eq < UserX | ('knows' : KnownSecrets , ..) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) = < UserX | ('knows' : (Secret , KnownSecrets) , ..) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : nils , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('owners' : (Owner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'join' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX , Owner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r9: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : nils , ...) , ....) > if CurrentTime - IssuedTime > 2 .`

## 48b9b769ac60.json (run2)

effect acc 100.0 rec 100.0; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  | exact |  |  |  |
| r8 |  |  |  |  |  |  | effect |  |  |
| r9 |  |  |  |  |  |  |  | effect |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | (...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | (...) > $ DeviceY 'callAPI:setKey' cloudA | (randomStr('Secret', N)) .`
- g4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : SetX , ...) , ....) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (SetX , ('key' : KeyA , 'time' : CurrentTime)) , ...) , ....) > .`
- g5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ UserX 'callAPI:getKey' cloudA | (DeviceY) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ cloudA 'send' UserX | (KeyA) if CurrentTime < TimeA + 1 .`
- g6: `eq < cloudA | (DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g7: `eq < cloudA | (DeviceY : ('owner' : SetX , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (SetX , UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g8: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : nils , ....) , .....) > if CurrentTime > TimeA + 2 .`
- g9: `eq < UserX | ('knowledge' : SetX , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('knowledge' : (SetX , KeyA) , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | (...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | (...) > $ deviceB 'uploadSecret' cloudA | (randomStr('Secret', N)) .`
- r4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : Tickets , ...) , ....) > $ deviceB 'uploadSecret' cloudA | (Secret) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : CurrentTime) , Tickets) , ...) , ....) > .`
- r5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ...) , ....) > $ UserX 'getKey' cloudA | (deviceB) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ...) , ....) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) if IssuedTime == CurrentTime .`
- r6: `eq < UserX | ('knowledge' : Knowledge , ..) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) = < UserX | ('knowledge' : (Secret , Knowledge) , ..) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : nils , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('owners' : (UserY , Owners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ..) , ...) > $ UserX 'join' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX , UserY , Owners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ..) , ...) > .`
- r9: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , Tickets) , ...) , ....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : nils , ...) , ....) > if CurrentTime - IssuedTime > 2 .`

## a348fcde5ba3.json (run3)

effect acc 100.0 rec 100.0; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  | exact |  |  |  |
| r8 |  |  |  |  |  |  | effect |  |  |
| r9 |  |  |  |  |  |  |  | effect |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | (...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | (...) > $ DeviceY 'callAPI:setKey' cloudA | (randomStr('Secret', N)) .`
- g4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : SetX , ...) , ....) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (SetX , ('key' : KeyA , 'time' : CurrentTime)) , ...) , ....) > .`
- g5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ UserX 'callAPI:getKey' cloudA | (DeviceY) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ cloudA 'send' UserX | (KeyA) if CurrentTime < TimeA + 1 .`
- g6: `eq < cloudA | (DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g7: `eq < cloudA | (DeviceY : ('owner' : SetX , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (SetX , UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g8: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : nils , ....) , .....) > if CurrentTime > TimeA + 2 .`
- g9: `eq < UserX | ('knowledge' : SetX , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('knowledge' : (SetX , KeyA) , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | (...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | (...) > $ deviceB 'uploadSecret' cloudA | (deviceB ; randomStr('Secret', N)) .`
- r4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : Tickets , ...) , ....) > $ deviceB 'uploadSecret' cloudA | (deviceB ; Secret) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : CurrentTime) , Tickets) , ...) , ....) > .`
- r5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ UserX 'getKey' cloudA | (deviceB) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) if IssuedTime == CurrentTime .`
- r6: `eq < UserX | ('knowledge' : Knowledge , ..) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) = < UserX | ('knowledge' : (Secret , Knowledge) , ..) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : nils , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('owners' : (UserOwner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'join' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX , UserOwner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r9: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : nils , ...) , ....) > if CurrentTime - IssuedTime > 2 .`

## cb6b8f998b16.json (run4)

effect acc 77.8 rec 77.8; exact acc 22.2 rec 44.4

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  |  |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  | effect |  |  |  |
| r8 |  |  |  |  |  |  | effect |  |  |
| r9 |  |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | (...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | (...) > $ DeviceY 'callAPI:setKey' cloudA | (randomStr('Secret', N)) .`
- g4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : SetX , ...) , ....) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (SetX , ('key' : KeyA , 'time' : CurrentTime)) , ...) , ....) > .`
- g5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ UserX 'callAPI:getKey' cloudA | (DeviceY) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ cloudA 'send' UserX | (KeyA) if CurrentTime < TimeA + 1 .`
- g6: `eq < cloudA | (DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g7: `eq < cloudA | (DeviceY : ('owner' : SetX , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (SetX , UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g8: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : nils , ....) , .....) > if CurrentTime > TimeA + 2 .`
- g9: `eq < UserX | ('knowledge' : SetX , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('knowledge' : (SetX , KeyA) , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | (...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | (...) > $ deviceB 'uploadSecret' cloudA | (randomStr('Secret', N)) .`
- r4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : Tickets , ...) , ....) > $ deviceB 'uploadSecret' cloudA | (Secret) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : ((Secret , CurrentTime) , Tickets) , ...) , ....) > .`
- r5: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : ((Secret , CurrentTime) , RestTickets) , ...) , ....) > $ UserX 'getKey' cloudA | (deviceB) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : ((Secret , CurrentTime) , RestTickets) , ...) , ....) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) .`
- r6: `eq < UserX | ('knows' : Knowledge , ..) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) = < UserX | ('knows' : (Secret , Knowledge) , ..) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : nils , 'tickets' : ((Secret , IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX) , 'tickets' : ((Secret , IssuedTime) , RestTickets) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('owners' : (UserOwner , RestOwners) , 'tickets' : ((Secret , IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'join' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX , UserOwner , RestOwners) , 'tickets' : ((Secret , IssuedTime) , RestTickets) , ..) , ...) > .`
- r9: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : ((Secret , IssuedTime) , RestTickets) , ...) , ....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : nils , ...) , ....) > if CurrentTime - IssuedTime > 2 .`

## 74ad357d17e7.json (run5)

effect acc 100.0 rec 100.0; exact acc 44.4 rec 66.7

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 |
|---|---|---|---|---|---|---|---|---|---|
| r1 | exact (gen wider) |  |  |  |  |  |  |  |  |
| r2 |  | exact (gen wider) |  |  |  |  |  |  |  |
| r3 |  |  | exact |  |  |  |  |  |  |
| r4 |  |  |  | exact |  |  |  |  |  |
| r5 |  |  |  |  | effect |  |  |  |  |
| r6 |  |  |  |  |  |  |  |  | exact |
| r7 |  |  |  |  |  | exact |  |  |  |
| r8 |  |  |  |  |  |  | effect |  |  |
| r9 |  |  |  |  |  |  |  | effect |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < system | ('counter' : N , ..) > < DeviceY | (...) > $ UserX 'pressButton' DeviceY = < system | ('counter' : N + 1 , ..) > < DeviceY | (...) > $ DeviceY 'callAPI:setKey' cloudA | (randomStr('Secret', N)) .`
- g4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : SetX , ...) , ....) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (SetX , ('key' : KeyA , 'time' : CurrentTime)) , ...) , ....) > .`
- g5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ UserX 'callAPI:getKey' cloudA | (DeviceY) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > $ cloudA 'send' UserX | (KeyA) if CurrentTime < TimeA + 1 .`
- g6: `eq < cloudA | (DeviceY : ('owner' : nils , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g7: `eq < cloudA | (DeviceY : ('owner' : SetX , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > $ UserX 'callAPI:join' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('owner' : (SetX , UserX) , 'tickets' : (('key' : KeyA , 'time' : TimeA) , ..) , ...) , ....) > .`
- g8: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : (('key' : KeyA , 'time' : TimeA) , ...) , ....) , .....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (DeviceY : ('tickets' : nils , ....) , .....) > if CurrentTime > TimeA + 2 .`
- g9: `eq < UserX | ('knowledge' : SetX , ..) > $ cloudA 'send' UserX | (KeyA) = < UserX | ('knowledge' : (SetX , KeyA) , ..) > .`

Generated rules (names as generated):

- r1: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r2: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`
- r3: `eq < system | ('counter' : N , ..) > < deviceB | (...) > $ UserX 'pressButton' deviceB = < system | ('counter' : N + 1 , ..) > < deviceB | (...) > $ deviceB 'uploadSecret' cloudA | (randomStr('Secret', N)) .`
- r4: `eq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : Tickets , ...) , ....) > $ deviceB 'uploadSecret' cloudA | (Secret) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : CurrentTime) , Tickets) , ...) , ....) > .`
- r5: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ UserX 'getKey' cloudA | (deviceB) = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) if IssuedTime == CurrentTime .`
- r6: `eq < UserX | ('knows' : KnownSecrets , ..) > $ cloudA 'sendSecret' UserX | (deviceB ; Secret) = < UserX | ('knows' : (Secret , KnownSecrets) , ..) > .`
- r7: `eq < cloudA | (deviceB : ('owners' : nils , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r8: `eq < cloudA | (deviceB : ('owners' : (UserOwner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > $ UserX 'join' cloudA | (deviceB ; Secret) = < cloudA | (deviceB : ('owners' : (UserX , UserOwner , RestOwners) , 'tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ..) , ...) > .`
- r9: `ceq < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : (('secret' : Secret , 'time' : IssuedTime) , RestTickets) , ...) , ....) > = < system | ('time' : CurrentTime , 'counter' : N , ..) > < cloudA | (deviceB : ('tickets' : nils , ...) , ....) > if CurrentTime - IssuedTime > 2 .`

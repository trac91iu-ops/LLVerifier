# iRobot: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## daad6387a6c4.json (a2-run5)

effect acc 100.0 rec 100.0; exact acc 77.8 rec 90.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 | g10 |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |  |  |  |
| r2 |  |  |  | exact (gen wider) | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |  |  |
| r4 |  |  |  |  |  |  |  | exact (gen narrower) |  |  |
| r5 |  |  |  |  |  |  |  |  | exact |  |
| r6 |  |  |  |  |  |  | exact |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  | exact |
| r8 | exact (gen wider) |  |  |  |  |  |  |  |  |  |
| r9 |  | exact (gen wider) |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g5: `eq < DeviceY | ('pressed' : true , 'key' : KeyB , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g6: `eq < cloudA | (DeviceY : ('bdKey' : KeyB , ..) , ...) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`
- g8: `eq < DeviceY | ('pressed' : true , 'key' : KeyA , ..) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('pressed' : false , .. , 'key' : KeyA) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g9: `eq < UserX | ('key' : KeyB , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g10: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : '' , 'owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : OldKey , ..) > $ UserX 'setKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : OldKey , ..) , ...) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , ..) , ...) > .`
- r4: `ceq < deviceB | ('buttonPressed' : true , 'key' : Key , ..) > $ UserX 'retrieveKey' deviceB = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) if Key =/= nils .`
- r5: `eq < UserX | ('key' : OldKey , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r6: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bind' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > $ UserX 'reset' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : '' , 'owner' : nils , ..) , ...) > .`
- r8: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r9: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 34fd55caae03.json (run1)

effect acc 100.0 rec 100.0; exact acc 77.8 rec 90.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 | g10 |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |  |  |  |
| r2 |  |  |  | exact (gen wider) | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |  |  |
| r4 |  |  |  |  |  |  |  | exact (gen narrower) |  |  |
| r5 |  |  |  |  |  |  |  |  | exact |  |
| r6 |  |  |  |  |  |  | exact |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  | exact |
| r8 | exact (gen wider) |  |  |  |  |  |  |  |  |  |
| r9 |  | exact (gen wider) |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g5: `eq < DeviceY | ('pressed' : true , 'key' : KeyB , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g6: `eq < cloudA | (DeviceY : ('bdKey' : KeyB , ..) , ...) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`
- g8: `eq < DeviceY | ('pressed' : true , 'key' : KeyA , ..) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('pressed' : false , .. , 'key' : KeyA) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g9: `eq < UserX | ('key' : KeyB , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g10: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : '' , 'owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : OldKey , ..) > $ UserX 'setKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : OldKey , ..) , ...) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , ..) , ...) > .`
- r4: `ceq < deviceB | ('buttonPressed' : true , 'key' : Key , ..) > $ UserX 'retrieveKey' deviceB = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) if Key =/= nils .`
- r5: `eq < UserX | ('key' : OldKey , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r6: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : '' , 'owner' : nils , ..) , ...) > .`
- r8: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r9: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 8db90940b376.json (run3)

effect acc 100.0 rec 100.0; exact acc 77.8 rec 90.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 | g10 |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |  |  |  |
| r2 |  |  |  | exact (gen wider) | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |  |  |
| r4 |  |  |  |  |  |  |  | exact (gen narrower) |  |  |
| r5 |  |  |  |  |  |  |  |  | exact |  |
| r6 |  |  |  |  |  |  | exact |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  | exact |
| r8 | exact (gen wider) |  |  |  |  |  |  |  |  |  |
| r9 |  | exact (gen wider) |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g5: `eq < DeviceY | ('pressed' : true , 'key' : KeyB , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g6: `eq < cloudA | (DeviceY : ('bdKey' : KeyB , ..) , ...) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`
- g8: `eq < DeviceY | ('pressed' : true , 'key' : KeyA , ..) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('pressed' : false , .. , 'key' : KeyA) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g9: `eq < UserX | ('key' : KeyB , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g10: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : '' , 'owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : OldKey , ..) > $ UserX 'setKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : OldKey , ..) , ...) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , ..) , ...) > .`
- r4: `ceq < deviceB | ('buttonPressed' : true , 'key' : Key , ..) > $ UserX 'retrieveKey' deviceB = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) if Key =/= nils .`
- r5: `eq < UserX | ('key' : OldKey , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r6: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : '' , 'owner' : nils , ..) , ...) > .`
- r8: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r9: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 72e89953abca.json (run4)

effect acc 100.0 rec 100.0; exact acc 77.8 rec 90.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 | g10 |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |  |  |  |
| r2 |  |  |  | exact (gen wider) | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |  |  |
| r4 |  |  |  |  |  |  |  | exact (gen narrower) |  |  |
| r5 |  |  |  |  |  |  |  |  | exact |  |
| r6 |  |  |  |  |  |  | exact |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  | exact |
| r8 | exact (gen wider) |  |  |  |  |  |  |  |  |  |
| r9 |  | exact (gen wider) |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g5: `eq < DeviceY | ('pressed' : true , 'key' : KeyB , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g6: `eq < cloudA | (DeviceY : ('bdKey' : KeyB , ..) , ...) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`
- g8: `eq < DeviceY | ('pressed' : true , 'key' : KeyA , ..) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('pressed' : false , .. , 'key' : KeyA) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g9: `eq < UserX | ('key' : KeyB , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g10: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : '' , 'owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : OldKey , ..) > $ UserX 'setKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : OldKey , ..) , ...) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , ..) , ...) > .`
- r4: `ceq < deviceB | ('buttonPressed' : true , 'key' : Key , ..) > $ UserX 'retrieveKey' deviceB = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) if Key =/= nils .`
- r5: `eq < UserX | ('key' : OldKey , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r6: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : '' , 'owner' : nils , ..) , ...) > .`
- r8: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r9: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

## 8eb3589ee396.json (run2)

effect acc 100.0 rec 100.0; exact acc 77.8 rec 90.0

| gen \ gold | g1 | g2 | g3 | g4 | g5 | g6 | g7 | g8 | g9 | g10 |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 |  |  | exact |  |  |  |  |  |  |  |
| r2 |  |  |  | exact (gen wider) | exact |  |  |  |  |  |
| r3 |  |  |  |  |  | exact |  |  |  |  |
| r4 |  |  |  |  |  |  |  | exact (gen narrower) |  |  |
| r5 |  |  |  |  |  |  |  |  | exact |  |
| r6 |  |  |  |  |  |  | exact |  |  |  |
| r7 |  |  |  |  |  |  |  |  |  | exact |
| r8 | exact (gen wider) |  |  |  |  |  |  |  |  |  |
| r9 |  | exact (gen wider) |  |  |  |  |  |  |  |  |

Gold rules:

- g1: `eq < UserX | ('localTo' : nils , ..) > $ UserX 'approaches' DeviceY = < UserX | ('localTo' : DeviceY , ..) > .`
- g2: `eq < UserX | ('localTo' : DeviceY , ..) > $ UserX 'leaves' DeviceY = < UserX | ('localTo' : nils , ..) > .`
- g3: `eq < DeviceY | ('pressed' : false , ..) > $ UserX 'pressButton' DeviceY = < DeviceY | ('pressed' : true , ..) > .`
- g4: `eq < DeviceY | ('pressed' : true , 'key' : nils , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g5: `eq < DeviceY | ('pressed' : true , 'key' : KeyB , ..) > $ UserX 'callAPI:setKey' DeviceY | (KeyA) = < DeviceY | ('pressed' : false , 'key' : KeyA , ..) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) .`
- g6: `eq < cloudA | (DeviceY : ('bdKey' : KeyB , ..) , ...) > $ DeviceY 'callAPI:setKey' cloudA | (KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , ..) , ...) > .`
- g7: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : nils , ..) , ...) > $ UserX 'callAPI:bind' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > .`
- g8: `eq < DeviceY | ('pressed' : true , 'key' : KeyA , ..) > $ UserX 'callAPI:getKey' DeviceY = < DeviceY | ('pressed' : false , .. , 'key' : KeyA) > $ DeviceY 'sendKey' UserX | (KeyA) .`
- g9: `eq < UserX | ('key' : KeyB , ..) > $ DeviceY 'sendKey' UserX | (KeyA) = < UserX | ('key' : KeyA , ..) > .`
- g10: `eq < cloudA | (DeviceY : ('bdKey' : KeyA , 'owner' : UserX , ..) , ...) > $ UserX 'callAPI:reset' cloudA | (DeviceY ; KeyA) = < cloudA | (DeviceY : ('bdKey' : '' , 'owner' : nils , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < deviceB | ('buttonPressed' : false , ..) > $ UserX 'pressButton' deviceB = < deviceB | ('buttonPressed' : true , ..) > .`
- r2: `eq < deviceB | ('buttonPressed' : true , 'key' : OldKey , ..) > $ UserX 'setKey' deviceB | (Key) = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) .`
- r3: `eq < cloudA | (deviceB : ('bindingKey' : OldKey , ..) , ...) > $ deviceB 'sendBindingKey' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , ..) , ...) > .`
- r4: `ceq < deviceB | ('buttonPressed' : true , 'key' : Key , ..) > $ UserX 'retrieveKey' deviceB = < deviceB | ('buttonPressed' : false , 'key' : Key , ..) > $ deviceB 'sendKey' UserX | (Key) if Key =/= nils .`
- r5: `eq < UserX | ('key' : OldKey , ..) > $ deviceB 'sendKey' UserX | (Key) = < UserX | ('key' : Key , ..) > .`
- r6: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : nils , ..) , ...) > $ UserX 'bindDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > .`
- r7: `eq < cloudA | (deviceB : ('bindingKey' : Key , 'owner' : UserX , ..) , ...) > $ UserX 'resetDevice' cloudA | (deviceB ; Key) = < cloudA | (deviceB : ('bindingKey' : '' , 'owner' : nils , ..) , ...) > .`
- r8: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'approach' deviceB = < UserX | ('near' : deviceB , ..) > .`
- r9: `eq < UserX | ('near' : OldNear , ..) > $ UserX 'leave' deviceB = < UserX | ('near' : nils , ..) > .`

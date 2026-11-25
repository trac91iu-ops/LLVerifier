# MQTTFlaw1: state rules, generated vs. gold

Cell = how generated rule r matches gold rule g. effect: same trigger, updates and emitted messages. exact: also the same guards. gen narrower: the generated rule requires more (precise but does not recall g). gen wider: the generated rule requires less (recalls g but is not precise).

## 963e09c7badf.json (run1)

effect acc 75.0 rec 75.0; exact acc 25.0 rec 50.0

| gen \ gold | g1 | g2 | g3 | g4 |
|---|---|---|---|---|
| r1 |  |  |  |  |
| r2 |  |  |  | exact (gen wider) |
| r3 |  |  | exact (gen narrower) |  |
| r4 | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : false , .. ) > $ cloudB 'device:publish' deviceB | ('toggle') = < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : true , .. ) > .`
- g2: `eq < cloudB | ('storedMessages' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'cloud:publish' cloudB | (MessageY) = < cloudB | ('storedMessages' : (MessageY) , UserX : ('permission' : true , ..) , ...) > $ cloudB 'user:pubrec' UserX .`
- g3: `eq < cloudB | ('storedMessages' : (MessageX) , DeviceY : ('permission' : true , ...) , ....) > $ UserX 'cloud:pubrel' cloudB = < cloudB | ('storedMessages' : nils , DeviceY : ('permission' : true , ...) , ....) > $ cloudB 'device:publish' DeviceY | (MessageX) .`
- g4: `eq < cloudB | (UserX : ('permission' : true , ..) , ...) > $ cloudB 'cloud:revoke' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < cloudB | ('buffer' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'requestPublish' cloudB | ('toggle') = < cloudB | ('buffer' : 'toggle' , UserX : ('permission' : true , ..) , ...) > $ cloudB 'acknowledge' UserX .`
- r2: `eq < cloudB | (UserX : ('permission' : OldPermission , ..) , ...) > $ cloudB 'revokePermission' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`
- r3: `ceq < cloudB | ('buffer' : Message , deviceB : ('permission' : true , ..) , ...) > $ UserX 'requestRelease' cloudB = < cloudB | ('buffer' : nils , deviceB : ('permission' : true , ..) , ...) > $ cloudB 'publish' deviceB | (Message) if Message =/= nils .`
- r4: `eq < deviceB | ('on' : false , ..) > $ cloudB 'publish' deviceB | ('toggle') = < deviceB | ('on' : true , ..) > .`

## 4dcfc0cea588.json (run2)

effect acc 75.0 rec 75.0; exact acc 25.0 rec 50.0

| gen \ gold | g1 | g2 | g3 | g4 |
|---|---|---|---|---|
| r1 |  |  |  |  |
| r2 |  |  |  | exact (gen wider) |
| r3 |  |  | exact (gen narrower) |  |
| r4 | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : false , .. ) > $ cloudB 'device:publish' deviceB | ('toggle') = < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : true , .. ) > .`
- g2: `eq < cloudB | ('storedMessages' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'cloud:publish' cloudB | (MessageY) = < cloudB | ('storedMessages' : (MessageY) , UserX : ('permission' : true , ..) , ...) > $ cloudB 'user:pubrec' UserX .`
- g3: `eq < cloudB | ('storedMessages' : (MessageX) , DeviceY : ('permission' : true , ...) , ....) > $ UserX 'cloud:pubrel' cloudB = < cloudB | ('storedMessages' : nils , DeviceY : ('permission' : true , ...) , ....) > $ cloudB 'device:publish' DeviceY | (MessageX) .`
- g4: `eq < cloudB | (UserX : ('permission' : true , ..) , ...) > $ cloudB 'cloud:revoke' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < cloudB | ('buffer' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'publishToggle' cloudB = < cloudB | ('buffer' : 'toggle' , UserX : ('permission' : true , ..) , ...) > $ cloudB 'acknowledgeReceipt' UserX .`
- r2: `eq < cloudB | (UserX : ('permission' : Permission , ..) , ...) > $ cloudB 'revokePermission' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`
- r3: `ceq < cloudB | ('buffer' : Message , deviceB : ('permission' : true , ..) , ...) > $ UserX 'releaseBufferedMessage' cloudB = < cloudB | ('buffer' : nils , deviceB : ('permission' : true , ..) , ...) > $ cloudB 'publishMessage' deviceB | (Message) if Message =/= nils .`
- r4: `eq < deviceB | ('on' : false , ..) > $ cloudB 'publishMessage' deviceB | ('toggle') = < deviceB | ('on' : true , ..) > .`

## 3858ddfc4107.json (run3)

effect acc 25.0 rec 25.0; exact acc 0.0 rec 25.0

| gen \ gold | g1 | g2 | g3 | g4 |
|---|---|---|---|---|
| r1 |  |  |  |  |
| r2 |  |  |  | exact (gen wider) |
| r3 |  |  |  |  |
| r4 |  |  |  |  |

Gold rules:

- g1: `eq < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : false , .. ) > $ cloudB 'device:publish' deviceB | ('toggle') = < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : true , .. ) > .`
- g2: `eq < cloudB | ('storedMessages' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'cloud:publish' cloudB | (MessageY) = < cloudB | ('storedMessages' : (MessageY) , UserX : ('permission' : true , ..) , ...) > $ cloudB 'user:pubrec' UserX .`
- g3: `eq < cloudB | ('storedMessages' : (MessageX) , DeviceY : ('permission' : true , ...) , ....) > $ UserX 'cloud:pubrel' cloudB = < cloudB | ('storedMessages' : nils , DeviceY : ('permission' : true , ...) , ....) > $ cloudB 'device:publish' DeviceY | (MessageX) .`
- g4: `eq < cloudB | (UserX : ('permission' : true , ..) , ...) > $ cloudB 'cloud:revoke' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < cloudB | ('buffer' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'publish' cloudB | ('toggle') = < cloudB | ('buffer' : 'toggle' , UserX : ('permission' : true , ..) , ...) > $ cloudB 'acknowledge' UserX .`
- r2: `eq < cloudB | (UserX : ('permission' : OldPermission , ..) , ...) > $ cloudB 'revokePermission' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`
- r3: `ceq < cloudB | ('buffer' : Message , deviceB : ('permission' : true , ..) , ...) > $ UserX 'release' cloudB = < cloudB | ('buffer' : nils , deviceB : ('permission' : true , ..) , ...) > $ cloudB 'publish' deviceB | (Message) if Message =/= nils .`
- r4: `eq < deviceB | ('on' : false , ..) > $ cloudB 'publish' deviceB | ('toggle') = < deviceB | ('on' : true , ..) > .`

## ef00ce4c44c0.json (run4)

effect acc 75.0 rec 75.0; exact acc 25.0 rec 50.0

| gen \ gold | g1 | g2 | g3 | g4 |
|---|---|---|---|---|
| r1 |  |  |  |  |
| r2 |  |  |  | exact (gen wider) |
| r3 |  |  | exact (gen narrower) |  |
| r4 | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : false , .. ) > $ cloudB 'device:publish' deviceB | ('toggle') = < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : true , .. ) > .`
- g2: `eq < cloudB | ('storedMessages' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'cloud:publish' cloudB | (MessageY) = < cloudB | ('storedMessages' : (MessageY) , UserX : ('permission' : true , ..) , ...) > $ cloudB 'user:pubrec' UserX .`
- g3: `eq < cloudB | ('storedMessages' : (MessageX) , DeviceY : ('permission' : true , ...) , ....) > $ UserX 'cloud:pubrel' cloudB = < cloudB | ('storedMessages' : nils , DeviceY : ('permission' : true , ...) , ....) > $ cloudB 'device:publish' DeviceY | (MessageX) .`
- g4: `eq < cloudB | (UserX : ('permission' : true , ..) , ...) > $ cloudB 'cloud:revoke' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < cloudB | ('buffer' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'requestPublish' cloudB | ('toggle') = < cloudB | ('buffer' : 'toggle' , UserX : ('permission' : true , ..) , ...) > $ cloudB 'acknowledgeReceipt' UserX .`
- r2: `eq < cloudB | (UserX : ('permission' : OldPermission , ..) , ...) > $ cloudB 'revokePermission' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`
- r3: `ceq < cloudB | ('buffer' : Message , deviceB : ('permission' : true , ..) , ...) > $ UserX 'requestRelease' cloudB = < cloudB | ('buffer' : nils , deviceB : ('permission' : true , ..) , ...) > $ cloudB 'publish' deviceB | (Message) if Message =/= nils .`
- r4: `eq < deviceB | ('on' : false , ..) > $ cloudB 'publish' deviceB | ('toggle') = < deviceB | ('on' : true , ..) > .`

## d04e4e5d57da.json (run5)

effect acc 75.0 rec 75.0; exact acc 25.0 rec 50.0

| gen \ gold | g1 | g2 | g3 | g4 |
|---|---|---|---|---|
| r1 |  |  |  |  |
| r2 |  |  |  | exact (gen wider) |
| r3 |  |  | exact (gen narrower) |  |
| r4 | exact (gen wider) |  |  |  |

Gold rules:

- g1: `eq < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : false , .. ) > $ cloudB 'device:publish' deviceB | ('toggle') = < cloudB | (deviceB : ('permission' : true , ...) , ....) > < deviceB | ('status' : true , .. ) > .`
- g2: `eq < cloudB | ('storedMessages' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'cloud:publish' cloudB | (MessageY) = < cloudB | ('storedMessages' : (MessageY) , UserX : ('permission' : true , ..) , ...) > $ cloudB 'user:pubrec' UserX .`
- g3: `eq < cloudB | ('storedMessages' : (MessageX) , DeviceY : ('permission' : true , ...) , ....) > $ UserX 'cloud:pubrel' cloudB = < cloudB | ('storedMessages' : nils , DeviceY : ('permission' : true , ...) , ....) > $ cloudB 'device:publish' DeviceY | (MessageX) .`
- g4: `eq < cloudB | (UserX : ('permission' : true , ..) , ...) > $ cloudB 'cloud:revoke' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`

Generated rules (names as generated):

- r1: `eq < cloudB | ('buffer' : nils , UserX : ('permission' : true , ..) , ...) > $ UserX 'requestPublish' cloudB | ('toggle') = < cloudB | ('buffer' : 'toggle' , UserX : ('permission' : true , ..) , ...) > $ cloudB 'acknowledgeReceipt' UserX .`
- r2: `eq < cloudB | (UserX : ('permission' : OldPermission , ..) , ...) > $ cloudB 'revokePermission' cloudB | (UserX) = < cloudB | (UserX : ('permission' : false , ..) , ...) > .`
- r3: `ceq < cloudB | ('buffer' : Message , deviceB : ('permission' : true , ..) , ...) > $ UserX 'requestRelease' cloudB = < cloudB | ('buffer' : nils , deviceB : ('permission' : true , ..) , ...) > $ cloudB 'publish' deviceB | (Message) if Message =/= nils .`
- r4: `eq < deviceB | ('on' : false , ..) > $ cloudB 'publish' deviceB | ('toggle') = < deviceB | ('on' : true , ..) > .`

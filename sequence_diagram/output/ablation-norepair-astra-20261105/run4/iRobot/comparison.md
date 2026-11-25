# iRobot

- input: `sequence_diagram/input/iRobot/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run4/iRobot/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (42 events); golden: counterexample (50 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceB : ('owner' : userC , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 2 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'setKey' deviceB | 'keyA'` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 4 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'retrieveKey' deviceB` |
| 5 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'bindDevice' cloudA | (deviceB ; 'keyA')` |
| 6 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 7 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'setKey' deviceB | 'keyA'` |
| 8 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `$ userA 'resetDevice' cloudA | (deviceB ; 'keyA')` |
| 9 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 10 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'retrieveKey' deviceB` |
| 11 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 12 | `$ userA 'approaches' deviceB` | `$ userA 'pressButton' deviceB` |
| 13 | `$ userC 'approaches' deviceB` | `$ userA 'setKey' deviceB | 'keyA'` |
| 14 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 15 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'setKey' deviceB | 'keyC'` |
| 16 | `$ userA 'leaves' deviceB` | `$ userA 'pressButton' deviceB` |
| 17 | `$ userC 'pressButton' deviceB` | `$ userA 'retrieveKey' deviceB` |
| 18 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceB` |
| 19 | `$ userC 'pressButton' deviceB` | `$ userA 'setKey' deviceB | 'keyC'` |
| 20 | `$ userC 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'bindDevice' cloudA | (deviceB ; 'keyC')` |
| 21 | `$ userC 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 22 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'setKey' deviceB | 'keyC'` |
| 23 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'resetDevice' cloudA | (deviceB ; 'keyC')` |
| 24 | `$ userC 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 25 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'retrieveKey' deviceB` |
| 26 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `$ userA 'leave' deviceB` |
| 27 | `$ userC 'leaves' deviceB` | `$ userC 'pressButton' deviceB` |
| 28 | `$ userA 'approaches' deviceB` | `$ userC 'setKey' deviceB | 'keyC'` |
| 29 | `$ userA 'pressButton' deviceB` | `$ userC 'pressButton' deviceB` |
| 30 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'retrieveKey' deviceB` |
| 31 | `$ userA 'leaves' deviceB` | `$ userA 'bindDevice' cloudA | (deviceB ; 'keyC')` |
| 32 | `$ userC 'approaches' deviceB` | `$ userC 'pressButton' deviceB` |
| 33 | `$ userA 'approaches' deviceB` | `$ userC 'setKey' deviceB | 'keyC'` |
| 34 | `$ userA 'pressButton' deviceB` | `$ userA 'resetDevice' cloudA | (deviceB ; 'keyC')` |
| 35 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'approach' deviceB` |
| 36 | `$ userA 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 37 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceB` |
| 38 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'setKey' deviceB | 'keyC'` |
| 39 | `$ userA 'pressButton' deviceB` | `$ userC 'bindDevice' cloudA | (deviceB ; 'keyC')` |
| 40 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceB` |
| 41 | `$ userA 'leaves' deviceB` | `$ userA 'setKey' deviceB | 'keyC'` |
| 42 | `$ userC 'leaves' deviceB` | `$ userC 'resetDevice' cloudA | (deviceB ; 'keyC')` |
| 43 | `$ userA 'approaches' deviceB` | `` |
| 44 | `$ userA 'pressButton' deviceB` | `` |
| 45 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |
| 46 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 47 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 48 | `$ userA 'pressButton' deviceB` | `` |
| 49 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 50 | `$ userC 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |

# iRobot

- input: `sequence_diagram/input/iRobot/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/iRobot/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (42 events); golden: counterexample (50 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceA , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceA : ('owner' : userC , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 2 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'setKey' deviceA | 'keyA'` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 4 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'getKey' deviceA` |
| 5 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'bind' cloudA | (deviceA ; 'keyA')` |
| 6 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 7 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'setKey' deviceA | 'keyA'` |
| 8 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `$ userA 'reset' cloudA | (deviceA ; 'keyA')` |
| 9 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 10 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'getKey' deviceA` |
| 11 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceA` |
| 12 | `$ userA 'approaches' deviceB` | `$ userA 'pressButton' deviceA` |
| 13 | `$ userC 'approaches' deviceB` | `$ userA 'setKey' deviceA | 'keyA'` |
| 14 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 15 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'setKey' deviceA | 'keyC'` |
| 16 | `$ userA 'leaves' deviceB` | `$ userA 'pressButton' deviceA` |
| 17 | `$ userC 'pressButton' deviceB` | `$ userA 'getKey' deviceA` |
| 18 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceA` |
| 19 | `$ userC 'pressButton' deviceB` | `$ userA 'setKey' deviceA | 'keyC'` |
| 20 | `$ userC 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'bind' cloudA | (deviceA ; 'keyC')` |
| 21 | `$ userC 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 22 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'setKey' deviceA | 'keyC'` |
| 23 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'reset' cloudA | (deviceA ; 'keyC')` |
| 24 | `$ userC 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 25 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'getKey' deviceA` |
| 26 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `$ userA 'leave' deviceA` |
| 27 | `$ userC 'leaves' deviceB` | `$ userC 'pressButton' deviceA` |
| 28 | `$ userA 'approaches' deviceB` | `$ userC 'setKey' deviceA | 'keyC'` |
| 29 | `$ userA 'pressButton' deviceB` | `$ userC 'pressButton' deviceA` |
| 30 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'getKey' deviceA` |
| 31 | `$ userA 'leaves' deviceB` | `$ userA 'bind' cloudA | (deviceA ; 'keyC')` |
| 32 | `$ userC 'approaches' deviceB` | `$ userC 'pressButton' deviceA` |
| 33 | `$ userA 'approaches' deviceB` | `$ userC 'setKey' deviceA | 'keyC'` |
| 34 | `$ userA 'pressButton' deviceB` | `$ userA 'reset' cloudA | (deviceA ; 'keyC')` |
| 35 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `$ userA 'approach' deviceA` |
| 36 | `$ userA 'pressButton' deviceB` | `$ userC 'leave' deviceA` |
| 37 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceA` |
| 38 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `$ userA 'setKey' deviceA | 'keyC'` |
| 39 | `$ userA 'pressButton' deviceB` | `$ userC 'bind' cloudA | (deviceA ; 'keyC')` |
| 40 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'pressButton' deviceA` |
| 41 | `$ userA 'leaves' deviceB` | `$ userA 'setKey' deviceA | 'keyC'` |
| 42 | `$ userC 'leaves' deviceB` | `$ userC 'reset' cloudA | (deviceA ; 'keyC')` |
| 43 | `$ userA 'approaches' deviceB` | `` |
| 44 | `$ userA 'pressButton' deviceB` | `` |
| 45 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |
| 46 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 47 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 48 | `$ userA 'pressButton' deviceB` | `` |
| 49 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 50 | `$ userC 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |

# iRobot

- input: `sequence_diagram/input/iRobot/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/iRobot/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (50 events)
- slots false at init expected; true at init: []
- coverage issues: ['B4 (action, line 30): no event rule for the initiated message', 'B5 (action, line 36): no event rule for the initiated message']

## Generated slots
```
eq E @ S < userC | ('near' : deviceA , ..) > |= attackerLocal = true .
eq E @ S < cloudA | ('owner' : userC , ..) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 3 | `$ userA 'pressButton' deviceB` | `` |
| 4 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 5 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 6 | `$ userA 'pressButton' deviceB` | `` |
| 7 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 8 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |
| 9 | `$ userA 'pressButton' deviceB` | `` |
| 10 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 11 | `$ userA 'leaves' deviceB` | `` |
| 12 | `$ userA 'approaches' deviceB` | `` |
| 13 | `$ userC 'approaches' deviceB` | `` |
| 14 | `$ userA 'pressButton' deviceB` | `` |
| 15 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 16 | `$ userA 'leaves' deviceB` | `` |
| 17 | `$ userC 'pressButton' deviceB` | `` |
| 18 | `$ userC 'callAPI:getKey' deviceB` | `` |
| 19 | `$ userC 'pressButton' deviceB` | `` |
| 20 | `$ userC 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 21 | `$ userC 'pressButton' deviceB` | `` |
| 22 | `$ userC 'callAPI:getKey' deviceB` | `` |
| 23 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 24 | `$ userC 'pressButton' deviceB` | `` |
| 25 | `$ userC 'callAPI:getKey' deviceB` | `` |
| 26 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |
| 27 | `$ userC 'leaves' deviceB` | `` |
| 28 | `$ userA 'approaches' deviceB` | `` |
| 29 | `$ userA 'pressButton' deviceB` | `` |
| 30 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 31 | `$ userA 'leaves' deviceB` | `` |
| 32 | `$ userC 'approaches' deviceB` | `` |
| 33 | `$ userA 'approaches' deviceB` | `` |
| 34 | `$ userA 'pressButton' deviceB` | `` |
| 35 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 36 | `$ userA 'pressButton' deviceB` | `` |
| 37 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 38 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 39 | `$ userA 'pressButton' deviceB` | `` |
| 40 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 41 | `$ userA 'leaves' deviceB` | `` |
| 42 | `$ userC 'leaves' deviceB` | `` |
| 43 | `$ userA 'approaches' deviceB` | `` |
| 44 | `$ userA 'pressButton' deviceB` | `` |
| 45 | `$ userA 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |
| 46 | `$ userA 'callAPI:setKey' deviceB | 'secretA'` | `` |
| 47 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secretA')` | `` |
| 48 | `$ userA 'pressButton' deviceB` | `` |
| 49 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 50 | `$ userC 'callAPI:reset' cloudA | (deviceB ; 'secretA')` | `` |

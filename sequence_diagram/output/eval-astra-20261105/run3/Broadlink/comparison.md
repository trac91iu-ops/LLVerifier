# Broadlink

- input: `sequence_diagram/input/Broadlink/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run3/Broadlink/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (53 events); golden: counterexample (21 events)
- slots false at init expected; true at init: []
- coverage issues: ['B7 (action, line 39): no event rule for the initiated message', 'B8 (action, line 45): no event rule for the initiated message']

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceB : ('owners' : (userC , Rest) , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userC 'approach' deviceB` |
| 2 | `$ userA 'pressButton' deviceB` | `$ userA 'leave' deviceB` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'approach' deviceB` |
| 4 | `$ userA 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 5 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'approach' deviceB` |
| 7 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'pressButton' deviceB` |
| 8 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 9 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'leave' deviceB` |
| 10 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'approach' deviceB` |
| 11 | `$ userA 'approaches' deviceB` | `$ userC 'leave' deviceB` |
| 12 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 13 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'approach' deviceB` |
| 14 | `$ userA 'callAPI:lock' deviceB | 'KeyB'362609376e` | `$ userA 'pressButton' deviceB` |
| 15 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'approach' deviceB` |
| 16 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'leave' deviceB` |
| 17 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 18 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'leave' deviceB` |
| 19 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'leave' deviceB` |
| 20 | `$ userC 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 21 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'KeyB'362609376e)` | `$ userA 'pressButton' deviceB` |
| 22 | `` | `$ userC 'approach' deviceB` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userA 'approach' deviceB` |
| 25 | `` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userA 'leave' deviceB` |
| 27 | `` | `$ userA 'approach' deviceB` |
| 28 | `` | `$ userA 'pressButton' deviceB` |
| 29 | `` | `$ userC 'approach' deviceB` |
| 30 | `` | `$ userA 'leave' deviceB` |
| 31 | `` | `$ userA 'approach' deviceB` |
| 32 | `` | `$ userC 'leave' deviceB` |
| 33 | `` | `$ userA 'leave' deviceB` |
| 34 | `` | `$ userA 'approach' deviceB` |
| 35 | `` | `$ userA 'retrieveKey' deviceB` |
| 36 | `` | `$ userC 'approach' deviceB` |
| 37 | `` | `$ userA 'leave' deviceB` |
| 38 | `` | `$ userA 'approach' deviceB` |
| 39 | `` | `$ userC 'leave' deviceB` |
| 40 | `` | `$ userA 'leave' deviceB` |
| 41 | `` | `$ userA 'approach' deviceB` |
| 42 | `` | `$ userA 'bind' cloudA | (deviceB ; 'Key'362609376e)` |
| 43 | `` | `$ userC 'approach' deviceB` |
| 44 | `` | `$ userA 'leave' deviceB` |
| 45 | `` | `$ userA 'approach' deviceB` |
| 46 | `` | `$ userC 'leave' deviceB` |
| 47 | `` | `$ userA 'leave' deviceB` |
| 48 | `` | `$ userC 'approach' deviceB` |
| 49 | `` | `$ userC 'retrieveKey' deviceB` |
| 50 | `` | `$ userA 'approach' deviceB` |
| 51 | `` | `$ userA 'leave' deviceB` |
| 52 | `` | `$ userC 'leave' deviceB` |
| 53 | `` | `$ userC 'bind' cloudA | (deviceB ; 'Key'362609376e)` |

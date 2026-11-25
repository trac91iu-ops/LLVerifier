# CloudEdgeCAC

- input: `sequence_diagram/input/CloudEdgeCAC/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run1/CloudEdgeCAC/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (64 events); golden: counterexample (7 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'leave' deviceB` |
| 2 | `$ userC 'pressButton' deviceD` | `$ userA 'approach' deviceB` |
| 3 | `$ userC 'callAPI:setKey' deviceD | 'phoneMacA'` | `$ userC 'leave' deviceD` |
| 4 | `$ userC 'pressButton' deviceD` | `$ userC 'approach' deviceB` |
| 5 | `$ userC 'callAPI:discover' deviceD` | `$ userA 'leave' deviceB` |
| 6 | `$ userA 'callAPI:setKey' deviceB | 'phoneMacC'` | `$ userA 'approach' deviceB` |
| 7 | `$ userA 'callAPI:discover' deviceB` | `$ userC 'leave' deviceB` |
| 8 | `` | `$ userC 'approach' deviceD` |
| 9 | `` | `$ userA 'pressButton' deviceB` |
| 10 | `` | `$ userA 'leave' deviceB` |
| 11 | `` | `$ userA 'approach' deviceB` |
| 12 | `` | `$ userC 'leave' deviceD` |
| 13 | `` | `$ userC 'approach' deviceB` |
| 14 | `` | `$ userA 'leave' deviceB` |
| 15 | `` | `$ userA 'approach' deviceB` |
| 16 | `` | `$ userC 'leave' deviceB` |
| 17 | `` | `$ userC 'approach' deviceD` |
| 18 | `` | `$ userC 'pressButton' deviceD` |
| 19 | `` | `$ userA 'leave' deviceB` |
| 20 | `` | `$ userA 'approach' deviceB` |
| 21 | `` | `$ userC 'leave' deviceD` |
| 22 | `` | `$ userC 'approach' deviceB` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userA 'approach' deviceB` |
| 25 | `` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userC 'approach' deviceD` |
| 27 | `` | `$ userC 'sendKey' deviceD | 'keyA'` |
| 28 | `` | `$ userA 'leave' deviceB` |
| 29 | `` | `$ userA 'approach' deviceB` |
| 30 | `` | `$ userC 'leave' deviceD` |
| 31 | `` | `$ userC 'approach' deviceB` |
| 32 | `` | `$ userA 'leave' deviceB` |
| 33 | `` | `$ userA 'approach' deviceB` |
| 34 | `` | `$ userC 'leave' deviceB` |
| 35 | `` | `$ userC 'approach' deviceD` |
| 36 | `` | `$ userC 'pressButton' deviceD` |
| 37 | `` | `$ userA 'leave' deviceB` |
| 38 | `` | `$ userA 'approach' deviceB` |
| 39 | `` | `$ userC 'leave' deviceD` |
| 40 | `` | `$ userC 'approach' deviceB` |
| 41 | `` | `$ userA 'leave' deviceB` |
| 42 | `` | `$ userA 'approach' deviceB` |
| 43 | `` | `$ userC 'leave' deviceB` |
| 44 | `` | `$ userC 'approach' deviceD` |
| 45 | `` | `$ userA 'sendKey' deviceB | 'keyC'` |
| 46 | `` | `$ userA 'discover' deviceB` |
| 47 | `` | `$ userA 'leave' deviceB` |
| 48 | `` | `$ userA 'approach' deviceB` |
| 49 | `` | `$ userC 'leave' deviceD` |
| 50 | `` | `$ userC 'approach' deviceB` |
| 51 | `` | `$ userA 'leave' deviceB` |
| 52 | `` | `$ userA 'approach' deviceB` |
| 53 | `` | `$ userC 'leave' deviceB` |
| 54 | `` | `$ userC 'approach' deviceD` |
| 55 | `` | `$ userA 'pressButton' deviceB` |
| 56 | `` | `$ userA 'leave' deviceB` |
| 57 | `` | `$ userA 'approach' deviceB` |
| 58 | `` | `$ userC 'leave' deviceD` |
| 59 | `` | `$ userC 'approach' deviceB` |
| 60 | `` | `$ userA 'leave' deviceB` |
| 61 | `` | `$ userA 'approach' deviceB` |
| 62 | `` | `$ userC 'leave' deviceB` |
| 63 | `` | `$ userC 'approach' deviceD` |
| 64 | `` | `$ userC 'discover' deviceD` |

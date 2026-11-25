# August

- input: `sequence_diagram/input/August/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run2/August/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (41 events); golden: counterexample (8 events)
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
| 1 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 2 | `$ userA 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 3 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 4 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 5 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userC 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 7 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'pressButton' deviceB` |
| 8 | `$ userC 'callAPI:reset' cloudA | deviceB` | `$ userC 'approach' deviceB` |
| 9 | `` | `$ userA 'leave' deviceB` |
| 10 | `` | `$ userA 'approach' deviceB` |
| 11 | `` | `$ userC 'leave' deviceB` |
| 12 | `` | `$ userA 'leave' deviceB` |
| 13 | `` | `$ userA 'approach' deviceB` |
| 14 | `` | `$ userA 'bind' cloudA | (deviceB ; 'keyB')` |
| 15 | `` | `$ userC 'approach' deviceB` |
| 16 | `` | `$ userA 'leave' deviceB` |
| 17 | `` | `$ userA 'approach' deviceB` |
| 18 | `` | `$ userC 'leave' deviceB` |
| 19 | `` | `$ userA 'leave' deviceB` |
| 20 | `` | `$ userA 'approach' deviceB` |
| 21 | `` | `$ userA 'reset' cloudA | deviceB` |
| 22 | `` | `$ userC 'approach' deviceB` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userA 'approach' deviceB` |
| 25 | `` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userA 'leave' deviceB` |
| 27 | `` | `$ userC 'approach' deviceB` |
| 28 | `` | `$ userC 'pressButton' deviceB` |
| 29 | `` | `$ userA 'approach' deviceB` |
| 30 | `` | `$ userA 'leave' deviceB` |
| 31 | `` | `$ userC 'leave' deviceB` |
| 32 | `` | `$ userC 'bind' cloudA | (deviceB ; 'keyB')` |
| 33 | `` | `$ userA 'approach' deviceB` |
| 34 | `` | `$ userC 'approach' deviceB` |
| 35 | `` | `$ userA 'leave' deviceB` |
| 36 | `` | `$ userA 'approach' deviceB` |
| 37 | `` | `$ userC 'leave' deviceB` |
| 38 | `` | `$ userA 'leave' deviceB` |
| 39 | `` | `$ userC 'approach' deviceB` |
| 40 | `` | `$ userC 'leave' deviceB` |
| 41 | `` | `$ userC 'reset' cloudA | deviceB` |

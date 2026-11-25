# CloudEdgeRTE

- input: `sequence_diagram/input/CloudEdgeRTE/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/CloudEdgeRTE/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (5 events); golden: counterexample (8 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | ('owner' : userC , ..) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'presses' deviceB` | `$ userC 'leave' deviceD` |
| 2 | `$ userC 'presses' deviceD` | `$ userA 'pressButton' deviceB` |
| 3 | `$ userA 'callAPI:setKey' deviceB | 'phoneMacA'` | `$ userA 'sendKey' deviceB | 'keyC'` |
| 4 | `$ userA 'presses' deviceB` | `$ userA 'discover' deviceB` |
| 5 | `$ userA 'callAPI:discover' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userC 'callAPI:setKey' deviceD | 'phoneMacA'` | `` |
| 7 | `$ userC 'callAPI:discover' deviceD` | `` |
| 8 | `$ userC 'presses' deviceD` | `` |

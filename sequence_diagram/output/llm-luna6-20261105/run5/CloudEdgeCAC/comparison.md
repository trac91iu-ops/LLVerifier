# CloudEdgeCAC

- input: `sequence_diagram/input/CloudEdgeCAC/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/CloudEdgeCAC/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (7 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userC 'pressButton' deviceD` | `` |
| 3 | `$ userC 'callAPI:setKey' deviceD | 'phoneMacA'` | `` |
| 4 | `$ userC 'pressButton' deviceD` | `` |
| 5 | `$ userC 'callAPI:discover' deviceD` | `` |
| 6 | `$ userA 'callAPI:setKey' deviceB | 'phoneMacC'` | `` |
| 7 | `$ userA 'callAPI:discover' deviceB` | `` |

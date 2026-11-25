# Imou

- input: `sequence_diagram/input/Imou/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run3/Imou/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (3 events); golden: counterexample (2 events)
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
| 1 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 2 | `$ userC 'pressButton' deviceB` | `$ userC 'buttonPress' deviceB` |
| 3 | `` | `$ userC 'bind' cloudA | 'keyB'` |

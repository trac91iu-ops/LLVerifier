# Ezviz

- input: `sequence_diagram/input/Ezviz/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run4/Ezviz/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (11 events); golden: counterexample (6 events)
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
| 6 | `$ userC 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 7 | `` | `$ userC 'pressButton' deviceB` |
| 8 | `` | `$ userA 'approach' deviceB` |
| 9 | `` | `$ userA 'leave' deviceB` |
| 10 | `` | `$ userC 'leave' deviceB` |
| 11 | `` | `$ userC 'bind' cloudA | 'keyB'` |

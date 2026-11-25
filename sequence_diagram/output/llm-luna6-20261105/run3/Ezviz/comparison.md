# Ezviz

- input: `sequence_diagram/input/Ezviz/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run3/Ezviz/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (6 events)
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
| 1 | `$ userA 'leaves' deviceB` | `` |
| 2 | `$ userA 'approaches' deviceB` | `` |
| 3 | `$ userC 'approaches' deviceB` | `` |
| 4 | `$ userC 'pressButton' deviceB` | `` |
| 5 | `$ userA 'leaves' deviceB` | `` |
| 6 | `$ userC 'leaves' deviceB` | `` |

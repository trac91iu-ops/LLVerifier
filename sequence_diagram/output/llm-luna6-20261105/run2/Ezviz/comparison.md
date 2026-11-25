# Ezviz

- input: `sequence_diagram/input/Ezviz/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/Ezviz/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (11 events); golden: counterexample (6 events)
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
| 1 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceA` |
| 2 | `$ userA 'approaches' deviceB` | `$ userA 'leave' deviceA` |
| 3 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceA` |
| 4 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceA` |
| 5 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceA` |
| 6 | `$ userC 'leaves' deviceB` | `$ userC 'approach' deviceA` |
| 7 | `` | `$ userC 'pressButton' deviceA` |
| 8 | `` | `$ userA 'approach' deviceA` |
| 9 | `` | `$ userA 'leave' deviceA` |
| 10 | `` | `$ userC 'leave' deviceA` |
| 11 | `` | `$ userC 'bind' cloudA | 'keyA'` |

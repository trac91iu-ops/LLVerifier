# Govee

- input: `sequence_diagram/input/Govee/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run5/Govee/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (14 events); golden: counterexample (6 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userC 'approach' deviceA` |
| 2 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceA` |
| 3 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceA` |
| 4 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceA` |
| 5 | `$ userC 'leaves' deviceB` | `$ userA 'leave' deviceA` |
| 6 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'approach' deviceA` |
| 7 | `` | `$ userA 'pressButton' deviceA` |
| 8 | `` | `$ userC 'approach' deviceA` |
| 9 | `` | `$ userA 'leave' deviceA` |
| 10 | `` | `$ userC 'leave' deviceA` |
| 11 | `` | `$ userC 'approach' deviceA` |
| 12 | `` | `$ userC 'pressButton' deviceA` |
| 13 | `` | `$ userC 'leave' deviceA` |
| 14 | `` | `$ userC 'bind' cloudA | (deviceA ; 'keyA')` |

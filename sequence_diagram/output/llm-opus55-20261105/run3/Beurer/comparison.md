# Beurer

- input: `sequence_diagram/input/Beurer/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/Beurer/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (18 events); golden: counterexample (8 events)
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
| 3 | `$ userA 'approaches' deviceB` | `$ userA 'approach' deviceA` |
| 4 | `$ userC 'approaches' deviceB` | `$ userC 'leave' deviceA` |
| 5 | `$ userC 'pressButton' deviceB` | `$ userA 'leave' deviceA` |
| 6 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceA` |
| 7 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceA` |
| 8 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'approach' deviceA` |
| 9 | `` | `$ userA 'leave' deviceA` |
| 10 | `` | `$ userA 'approach' deviceA` |
| 11 | `` | `$ userC 'leave' deviceA` |
| 12 | `` | `$ userA 'leave' deviceA` |
| 13 | `` | `$ userC 'approach' deviceA` |
| 14 | `` | `$ userC 'pressButton' deviceA` |
| 15 | `` | `$ userA 'approach' deviceA` |
| 16 | `` | `$ userA 'leave' deviceA` |
| 17 | `` | `$ userC 'leave' deviceA` |
| 18 | `` | `$ userC 'bind' cloudA | (deviceA ; 'keyA')` |

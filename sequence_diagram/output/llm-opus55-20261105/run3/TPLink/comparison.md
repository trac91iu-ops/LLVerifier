# TPLink

- input: `sequence_diagram/input/TPLink/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/TPLink/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (8 events); golden: counterexample (10 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceA` |
| 2 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceA` |
| 3 | `$ userA 'approaches' deviceB` | `$ userC 'sendKey' deviceA | 'keyC'` |
| 4 | `$ userC 'approaches' deviceB` | `$ userA 'pressButton' deviceA` |
| 5 | `$ userC 'callAPI:setKey' deviceB | 'secretC'` | `$ userA 'leave' deviceA` |
| 6 | `$ userA 'pressButton' deviceB` | `$ userA 'approach' deviceA` |
| 7 | `$ userA 'leaves' deviceB` | `$ userC 'leave' deviceA` |
| 8 | `$ userC 'leaves' deviceB` | `$ userA 'discover' deviceA` |
| 9 | `$ userA 'approaches' deviceB` | `` |
| 10 | `$ userA 'callAPI:discover' deviceB` | `` |

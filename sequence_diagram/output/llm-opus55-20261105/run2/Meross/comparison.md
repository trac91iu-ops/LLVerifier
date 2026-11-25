# Meross

- input: `sequence_diagram/input/Meross/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run2/Meross/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (7 events); golden: counterexample (8 events)
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
| 3 | `$ userA 'approaches' deviceB` | `$ userC 'pressButton' deviceA` |
| 4 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceA` |
| 5 | `$ userC 'pressButton' deviceB` | `$ userA 'approach' deviceA` |
| 6 | `$ userA 'leaves' deviceB` | `$ userC 'leave' deviceA` |
| 7 | `$ userC 'leaves' deviceB` | `$ userC 'bindDevice' cloudA | ('keyDevice' ; 'keyC')` |
| 8 | `$ userC 'callAPI:bind' cloudA | ('secret' ; 'UIDC')` | `` |

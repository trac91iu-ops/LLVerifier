# Meross

- input: `sequence_diagram/input/Meross/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/Meross/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (8 events)
- slots false at init expected; true at init: []
- coverage issues: ['B3 (action, line 22): no event rule for the initiated message']

## Generated slots
```
eq E @ S < userC | ('near' : deviceA , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceA : ('owner' : userC , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'leaves' deviceB` | `` |
| 3 | `$ userA 'approaches' deviceB` | `` |
| 4 | `$ userC 'approaches' deviceB` | `` |
| 5 | `$ userC 'pressButton' deviceB` | `` |
| 6 | `$ userA 'leaves' deviceB` | `` |
| 7 | `$ userC 'leaves' deviceB` | `` |
| 8 | `$ userC 'callAPI:bind' cloudA | ('secret' ; 'UIDC')` | `` |

# Wemo

- input: `sequence_diagram/input/Wemo/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Wemo/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (10 events)
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
| 1 | `$ userA 'press' deviceB` | `` |
| 2 | `$ userA 'leaves' deviceB` | `` |
| 3 | `$ userA 'approaches' deviceB` | `` |
| 4 | `$ userC 'approaches' deviceB` | `` |
| 5 | `$ userC 'callAPI:setKey' deviceB | 'secretC'` | `` |
| 6 | `$ userA 'press' deviceB` | `` |
| 7 | `$ userA 'leaves' deviceB` | `` |
| 8 | `$ userC 'leaves' deviceB` | `` |
| 9 | `$ userA 'approaches' deviceB` | `` |
| 10 | `$ userA 'callAPI:discover' deviceB` | `` |

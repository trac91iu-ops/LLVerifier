# TPLink

- input: `sequence_diagram/input/TPLink/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run5/TPLink/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (8 events); golden: counterexample (10 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 2 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 3 | `$ userA 'approaches' deviceB` | `$ userC 'sendKey' deviceB | 'keyC'` |
| 4 | `$ userC 'approaches' deviceB` | `$ userA 'pressButton' deviceB` |
| 5 | `$ userC 'callAPI:setKey' deviceB | 'secretC'` | `$ userA 'leave' deviceB` |
| 6 | `$ userA 'pressButton' deviceB` | `$ userA 'approach' deviceB` |
| 7 | `$ userA 'leaves' deviceB` | `$ userC 'leave' deviceB` |
| 8 | `$ userC 'leaves' deviceB` | `$ userA 'discover' deviceB` |
| 9 | `$ userA 'approaches' deviceB` | `` |
| 10 | `$ userA 'callAPI:discover' deviceB` | `` |

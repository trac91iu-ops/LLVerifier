# Govee

- input: `sequence_diagram/input/Govee/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Govee/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (14 events); golden: counterexample (6 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userC 'approach' deviceB` |
| 2 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 3 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 4 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 5 | `$ userC 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'approach' deviceB` |
| 7 | `` | `$ userA 'pressButton' deviceB` |
| 8 | `` | `$ userC 'approach' deviceB` |
| 9 | `` | `$ userA 'leave' deviceB` |
| 10 | `` | `$ userC 'leave' deviceB` |
| 11 | `` | `$ userC 'approach' deviceB` |
| 12 | `` | `$ userC 'pressButton' deviceB` |
| 13 | `` | `$ userC 'leave' deviceB` |
| 14 | `` | `$ userC 'bind' cloudA | (deviceB ; 'keyA')` |

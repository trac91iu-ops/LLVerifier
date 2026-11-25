# Beurer

- input: `sequence_diagram/input/Beurer/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run5/Beurer/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (18 events); golden: counterexample (8 events)
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
| 3 | `$ userA 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 4 | `$ userC 'approaches' deviceB` | `$ userC 'leave' deviceB` |
| 5 | `$ userC 'pressButton' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 7 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceB` |
| 8 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'approach' deviceB` |
| 9 | `` | `$ userA 'leave' deviceB` |
| 10 | `` | `$ userA 'approach' deviceB` |
| 11 | `` | `$ userC 'leave' deviceB` |
| 12 | `` | `$ userA 'leave' deviceB` |
| 13 | `` | `$ userC 'approach' deviceB` |
| 14 | `` | `$ userC 'pressButton' deviceB` |
| 15 | `` | `$ userA 'approach' deviceB` |
| 16 | `` | `$ userA 'leave' deviceB` |
| 17 | `` | `$ userC 'leave' deviceB` |
| 18 | `` | `$ userC 'bind' cloudA | (deviceB ; 'keyB')` |

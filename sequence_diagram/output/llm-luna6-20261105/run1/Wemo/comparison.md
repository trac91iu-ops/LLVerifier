# Wemo

- input: `sequence_diagram/input/Wemo/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run1/Wemo/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (11 events); golden: counterexample (10 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | ('owner' : userC , ..) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'press' deviceB` | `$ userA 'pressButton' deviceB` |
| 2 | `$ userA 'leaves' deviceB` | `$ userA 'discover' deviceB` |
| 3 | `$ userA 'approaches' deviceB` | `$ userC 'approach' deviceB` |
| 4 | `$ userC 'approaches' deviceB` | `$ userC 'sendKey' deviceB | 'accountKeyC'` |
| 5 | `$ userC 'callAPI:setKey' deviceB | 'secretC'` | `$ userA 'pressButton' deviceB` |
| 6 | `$ userA 'press' deviceB` | `$ userA 'leave' deviceB` |
| 7 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 8 | `$ userC 'leaves' deviceB` | `$ userC 'leave' deviceB` |
| 9 | `$ userA 'approaches' deviceB` | `$ userA 'discover' deviceB` |
| 10 | `$ userA 'callAPI:discover' deviceB` | `$ userC 'approach' deviceB` |
| 11 | `` | `$ userC 'discover' deviceB` |

# Sunlogin

- input: `sequence_diagram/input/Sunlogin/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/Sunlogin/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (6 events); golden: counterexample (6 events)
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
| 3 | `$ userC 'approaches' deviceB` | `$ userC 'pressButton' deviceB` |
| 4 | `$ userC 'pressButton' deviceB` | `$ userA 'leave' deviceB` |
| 5 | `$ userC 'leaves' deviceB` | `$ userC 'leave' deviceB` |
| 6 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'bindDevice' cloudA | (deviceB ; 'keyB')` |

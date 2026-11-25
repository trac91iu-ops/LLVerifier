# Meross

- input: `sequence_diagram/input/Meross/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/Meross/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (7 events); golden: counterexample (8 events)
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
| 3 | `$ userA 'approaches' deviceB` | `$ userC 'pressButton' deviceB` |
| 4 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 5 | `$ userC 'pressButton' deviceB` | `$ userA 'approach' deviceB` |
| 6 | `$ userA 'leaves' deviceB` | `$ userC 'leave' deviceB` |
| 7 | `$ userC 'leaves' deviceB` | `$ userC 'userBind' cloudA | ('keyB' ; 'keyC')` |
| 8 | `$ userC 'callAPI:bind' cloudA | ('secret' ; 'UIDC')` | `` |

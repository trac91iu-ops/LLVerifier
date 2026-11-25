# TuyaMatter

- input: `sequence_diagram/input/TuyaMatter/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run2/TuyaMatter/`
- property: CTRL-direct (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (7 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < cloudA | UserX : ('members' : Members , ...) , ... > $ UserX 'invite' cloudA |

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 2 | `$ userC 'callAPI:openWindow' cloudA | deviceB` | `` |
| 3 | `$ userC 'callAPI:bind' deviceB | 'KeyA'2357136044` | `` |
| 4 | `$ userA 'callAPI:openWindow' cloudA | deviceB` | `` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 6 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 7 | `$ userC 'callAPI:toggle' deviceB` | `` |

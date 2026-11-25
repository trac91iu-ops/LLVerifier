# TuyaCAC

- input: `sequence_diagram/input/TuyaCAC/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run4/TuyaCAC/`
- property: CTRL-direct (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (6 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < cloudA | UserX : ('members' : Members , ...) , ... > $ UserX 'invite' cloudA |

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `` |

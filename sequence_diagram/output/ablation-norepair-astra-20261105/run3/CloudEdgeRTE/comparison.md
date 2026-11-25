# CloudEdgeRTE

- input: `sequence_diagram/input/CloudEdgeRTE/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run3/CloudEdgeRTE/`
- property: OWN-remote (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (8 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < UserX | 'near' : Near , ... > $ UserX 'approach' DeviceX
=> < UserX | 'near' :

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'presses' deviceB` | `` |
| 2 | `$ userC 'presses' deviceD` | `` |
| 3 | `$ userA 'callAPI:setKey' deviceB | 'phoneMacA'` | `` |
| 4 | `$ userA 'presses' deviceB` | `` |
| 5 | `$ userA 'callAPI:discover' deviceB` | `` |
| 6 | `$ userC 'callAPI:setKey' deviceD | 'phoneMacA'` | `` |
| 7 | `$ userC 'callAPI:discover' deviceD` | `` |
| 8 | `$ userC 'presses' deviceD` | `` |

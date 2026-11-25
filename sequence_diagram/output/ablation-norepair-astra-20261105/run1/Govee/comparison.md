# Govee

- input: `sequence_diagram/input/Govee/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run1/Govee/`
- property: OWN-remote (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (6 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < UserX | 'near' : OldNear , 'key' : nils , ... > $ UserX 'approach' deviceB
=> 

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'leaves' deviceB` | `` |
| 3 | `$ userC 'approaches' deviceB` | `` |
| 4 | `$ userC 'pressButton' deviceB` | `` |
| 5 | `$ userC 'leaves' deviceB` | `` |
| 6 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `` |

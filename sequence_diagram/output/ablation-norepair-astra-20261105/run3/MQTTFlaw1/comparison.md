# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run3/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: failed; verdict: None (0 events); golden: counterexample (3 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < cloudB | 'buffer' : nils , UserX : ('permission' : true , ...) , ... > $ UserX

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `` |

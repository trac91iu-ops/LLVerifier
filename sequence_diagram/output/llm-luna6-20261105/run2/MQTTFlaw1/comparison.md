# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: validation_failed; verdict: None (0 events); golden: counterexample (3 events)
- slots false at init expected; true at init: None
- coverage issues: []

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `` |

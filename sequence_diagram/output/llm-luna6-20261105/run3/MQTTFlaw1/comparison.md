# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run3/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: failed; verdict: None (0 events); golden: counterexample (3 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 2 repairs: No terminal matches '.' in the current parser context, at line 1 col 25

< userA | nils > => ev1 .
                        ^
Expected one of: '\\('

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `` |

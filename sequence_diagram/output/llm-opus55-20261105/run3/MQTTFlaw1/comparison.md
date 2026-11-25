# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: validated; verdict: holds (0 events); golden: counterexample (3 events)
- slots false at init expected; true at init: ['attackerAuthorized']
- coverage issues: []

## Generated slots
```
eq E @ S < deviceA | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudB | (userA : ('permission' : true , ..) , ...) > |= attackerAuthorized = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `` |

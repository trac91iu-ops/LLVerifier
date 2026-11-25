# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run2/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: validated; verdict: holds (0 events); golden: counterexample (3 events)
- slots false at init expected; true at init: []
- coverage issues: ['B2 (action, line 18): no event rule for the initiated message']

## Generated slots
```
eq E @ S < deviceA | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudB | ('permission' : (userA , Rest) , ..) > |= attackerAuthorized = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `` |

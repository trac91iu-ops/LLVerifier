# MQTTFlaw1

- input: `sequence_diagram/input/MQTTFlaw1/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run1/MQTTFlaw1/`
- property: CTRL-revoked (attacker userA)
- status: validated; verdict: counterexample (3 events); golden: counterexample (3 events)
- slots false at init expected; true at init: ['attackerAuthorized']
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudB | (userA : ('permission' : true , ..) , ...) > |= attackerAuthorized = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'cloud:publish' cloudB | 'toggle'` | `$ userA 'requestPublish' cloudB | 'toggle'` |
| 2 | `$ cloudB 'cloud:revoke' cloudB | userA` | `$ cloudB 'revokePermission' cloudB | userA` |
| 3 | `$ userA 'cloud:pubrel' cloudB` | `$ userA 'requestRelease' cloudB` |

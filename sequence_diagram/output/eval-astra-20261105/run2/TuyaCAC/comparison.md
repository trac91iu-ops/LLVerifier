# TuyaCAC

- input: `sequence_diagram/input/TuyaCAC/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run2/TuyaCAC/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (6 events); golden: counterexample (6 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudA | (userC : ('device' : deviceB , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `$ userA 'invite' cloudA | userC` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'invite' cloudA | userA` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `$ userA 'requestKey' cloudA | deviceB` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'requestKey' cloudA | deviceB` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `$ userC 'turnOn' deviceB | 'keyB'` |

# TuyaCAC

- input: `sequence_diagram/input/TuyaCAC/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run3/TuyaCAC/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (6 events); golden: counterexample (6 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceA | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudA | (userC : ('device' : deviceA , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `$ userA 'invite' cloudA | userC` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'invite' cloudA | userA` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `$ userA 'requestKey' cloudA | deviceA` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'requestKey' cloudA | deviceA` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `$ userC 'turnOn' deviceA | 'keyA'` |

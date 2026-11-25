# TuyaCAC

- input: `sequence_diagram/input/TuyaCAC/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run4/TuyaCAC/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (6 events)
- slots false at init expected; true at init: ['attackerAuthorized']
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
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `` |

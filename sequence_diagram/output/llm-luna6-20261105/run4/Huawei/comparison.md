# Huawei

- input: `sequence_diagram/input/Huawei/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run4/Huawei/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (11 events)
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
| 7 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 8 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 9 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 11 | `$ userC 'callAPI:invite' cloudA | userA` | `` |

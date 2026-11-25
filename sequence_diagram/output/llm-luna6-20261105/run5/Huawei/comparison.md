# Huawei

- input: `sequence_diagram/input/Huawei/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Huawei/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (7 events); golden: counterexample (11 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudB | (userC : ('device' : deviceB , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `$ userA 'invite' cloudB | userC` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'invite' cloudB | userA` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `$ userA 'requestKey' cloudB | deviceB` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'requestKey' cloudB | deviceB` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'cloudTurnOn' cloudB | deviceB` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `$ userA 'removeMember' cloudB | userC` |
| 7 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'turnOn' deviceB | 'keyB'` |
| 8 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 9 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 11 | `$ userC 'callAPI:invite' cloudA | userA` | `` |

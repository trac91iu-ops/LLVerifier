# Xiaomi

- input: `sequence_diagram/input/Xiaomi/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run2/Xiaomi/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (11 events); golden: counterexample (11 events)
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
| 7 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 8 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 9 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userC 'removeMember' cloudA | userA` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 11 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'invite' cloudA | userA` |

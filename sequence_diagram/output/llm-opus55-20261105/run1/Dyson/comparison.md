# Dyson

- input: `sequence_diagram/input/Dyson/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run1/Dyson/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (11 events); golden: counterexample (11 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudA | (userC : ('device' : (deviceB , Rest) , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `$ userA 'inviteMember' cloudA | userC` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'inviteMember' cloudA | userA` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `$ userA 'requestKey' cloudA | deviceB` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'requestKey' cloudA | deviceB` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `$ userC 'turnOn' deviceB | 'keyB'` |
| 7 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'inviteMember' cloudA | userC` |
| 8 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 9 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userC 'removeMember' cloudA | userA` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'inviteMember' cloudA | userC` |
| 11 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'inviteMember' cloudA | userA` |

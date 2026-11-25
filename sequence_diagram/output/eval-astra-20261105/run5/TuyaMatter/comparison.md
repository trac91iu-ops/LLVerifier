# TuyaMatter

- input: `sequence_diagram/input/TuyaMatter/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run5/TuyaMatter/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (7 events); golden: counterexample (7 events)
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
| 1 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 2 | `$ userC 'callAPI:openWindow' cloudA | deviceB` | `$ userC 'invite' cloudA | userA` |
| 3 | `$ userC 'callAPI:bind' deviceB | 'KeyA'2357136044` | `$ userC 'openWindow' cloudA | deviceB` |
| 4 | `$ userA 'callAPI:openWindow' cloudA | deviceB` | `$ userA 'openWindow' cloudA | deviceB` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'bind' deviceB | 'Key'2357136044` |
| 6 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 7 | `$ userC 'callAPI:toggle' deviceB` | `$ userC 'turnOn' deviceB` |

# Aqara

- input: `sequence_diagram/input/Aqara/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run4/Aqara/`
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
| 2 | `$ userC 'callAPI:openWindow' cloudA | deviceB` | `$ userC 'openWindow' cloudA | deviceB` |
| 3 | `$ userC 'callAPI:bind' deviceB | 'KeyA'2357136044` | `$ userA 'openWindow' cloudA | deviceB` |
| 4 | `$ userA 'callAPI:openWindow' cloudA | deviceB` | `$ userC 'bind' deviceB | 'Key'2357136044` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'invite' cloudA | userA` |
| 6 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'remove' cloudA | userC` |
| 7 | `$ userC 'callAPI:toggle' deviceB` | `$ userC 'turnOn' deviceB` |

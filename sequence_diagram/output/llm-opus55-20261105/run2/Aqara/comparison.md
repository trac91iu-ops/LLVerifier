# Aqara

- input: `sequence_diagram/input/Aqara/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run2/Aqara/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (7 events); golden: counterexample (7 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceA | ('power' : 'on' , ..) > |= deviceOn = true .
eq E @ S < cloudA | (userC : ('device' : deviceA , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 2 | `$ userC 'callAPI:openWindow' cloudA | deviceB` | `$ userC 'openWindow' cloudA | deviceA` |
| 3 | `$ userC 'callAPI:bind' deviceB | 'KeyA'2357136044` | `$ userA 'openWindow' cloudA | deviceA` |
| 4 | `$ userA 'callAPI:openWindow' cloudA | deviceB` | `$ userC 'bind' deviceA | 'Key'2357136044` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'invite' cloudA | userA` |
| 6 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'kick' cloudA | userC` |
| 7 | `$ userC 'callAPI:toggle' deviceB` | `$ userC 'turnOn' deviceA` |

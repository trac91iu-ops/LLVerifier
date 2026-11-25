# TuyaMatter

- input: `sequence_diagram/input/TuyaMatter/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/TuyaMatter/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (7 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < deviceB | ('trusted' : (userC , Rest) , ..) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 2 | `$ userC 'callAPI:openWindow' cloudA | deviceB` | `` |
| 3 | `$ userC 'callAPI:bind' deviceB | 'KeyA'2357136044` | `` |
| 4 | `$ userA 'callAPI:openWindow' cloudA | deviceB` | `` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 6 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 7 | `$ userC 'callAPI:toggle' deviceB` | `` |

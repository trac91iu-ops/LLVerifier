# Switchbot

- input: `sequence_diagram/input/Switchbot/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run1/Switchbot/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (18 events); golden: counterexample (33 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceB : ('owners' : ((userC , Rest) , ..) , ...) , ....) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'invite' cloudA | userC` |
| 2 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'invite' cloudA | userA` |
| 3 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 4 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userC 'removeMember' cloudA | userA` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'approach' deviceB` |
| 6 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'pressButton' deviceB` |
| 7 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 8 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userC 'invite' cloudA | userA` |
| 9 | `$ userA 'leaves' deviceB` | `$ userA 'removeMember' cloudA | userC` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'removeMember' cloudA | userA` |
| 11 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'leave' deviceB` |
| 12 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'invite' cloudA | userC` |
| 13 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'invite' cloudA | userA` |
| 14 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 15 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userC 'removeMember' cloudA | userA` |
| 16 | `$ userA 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 17 | `$ userC 'approaches' deviceB` | `$ userC 'leave' deviceB` |
| 18 | `$ userC 'pressButton' deviceB` | `$ userC 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 19 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 20 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 21 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 22 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 23 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 24 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 25 | `$ userA 'leaves' deviceB` | `` |
| 26 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 27 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 28 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 29 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 30 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 31 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 32 | `$ userC 'leaves' deviceB` | `` |
| 33 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `` |

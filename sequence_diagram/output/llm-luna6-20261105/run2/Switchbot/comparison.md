# Switchbot

- input: `sequence_diagram/input/Switchbot/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/Switchbot/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (19 events); golden: counterexample (33 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceB : ('owners' : (userC , Rest) , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 2 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'invite' cloudA | userC` |
| 3 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'invite' cloudA | userA` |
| 4 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'removeMember' cloudA | userA` |
| 6 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'approach' deviceB` |
| 7 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userC 'pressButton' deviceB` |
| 8 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'invite' cloudA | userC` |
| 9 | `$ userA 'leaves' deviceB` | `$ userC 'invite' cloudA | userA` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'removeMember' cloudA | userC` |
| 11 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userC 'removeMember' cloudA | userA` |
| 12 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'leave' deviceB` |
| 13 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userA 'invite' cloudA | userC` |
| 14 | `$ userA 'callAPI:kick' cloudA | userC` | `$ userC 'invite' cloudA | userA` |
| 15 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'removeMember' cloudA | userC` |
| 16 | `$ userA 'approaches' deviceB` | `$ userC 'removeMember' cloudA | userA` |
| 17 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 18 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 19 | `$ userA 'callAPI:invite' cloudA | userC` | `$ userC 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
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

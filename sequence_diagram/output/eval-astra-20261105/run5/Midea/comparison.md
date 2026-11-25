# Midea

- input: `sequence_diagram/input/Midea/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run5/Midea/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (19 events); golden: counterexample (21 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceB , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceB : ('owner' : userC , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 2 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 3 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'resetDevice' cloudA | deviceB` |
| 4 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 5 | `$ userA 'approaches' deviceB` | `$ userA 'pressButton' deviceB` |
| 6 | `$ userC 'approaches' deviceB` | `$ userA 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 7 | `$ userA 'pressButton' deviceB` | `$ userA 'resetDevice' cloudA | deviceB` |
| 8 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'pressButton' deviceB` |
| 9 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 10 | `$ userC 'pressButton' deviceB` | `$ userA 'resetDevice' cloudA | deviceB` |
| 11 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'leave' deviceB` |
| 12 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'pressButton' deviceB` |
| 13 | `$ userA 'leaves' deviceB` | `$ userA 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 14 | `$ userC 'pressButton' deviceB` | `$ userA 'resetDevice' cloudA | deviceB` |
| 15 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'approach' deviceB` |
| 16 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'leave' deviceB` |
| 17 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceB` |
| 18 | `$ userA 'approaches' deviceB` | `$ userC 'bindDevice' cloudA | (deviceB ; 'deviceKey')` |
| 19 | `$ userA 'pressButton' deviceB` | `$ userC 'resetDevice' cloudA | deviceB` |
| 20 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `` |
| 21 | `$ userC 'callAPI:reset' cloudA` | `` |

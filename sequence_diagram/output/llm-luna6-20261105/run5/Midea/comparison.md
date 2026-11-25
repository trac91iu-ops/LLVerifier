# Midea

- input: `sequence_diagram/input/Midea/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Midea/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (32 events); golden: counterexample (21 events)
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
| 2 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 3 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'reset' cloudA | deviceB` |
| 4 | `$ userA 'leaves' deviceB` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 5 | `$ userA 'approaches' deviceB` | `$ userC 'approach' deviceB` |
| 6 | `$ userC 'approaches' deviceB` | `$ userA 'pressButton' deviceB` |
| 7 | `$ userA 'pressButton' deviceB` | `$ userA 'reset' cloudA | deviceB` |
| 8 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'pressButton' deviceB` |
| 9 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'leave' deviceB` |
| 10 | `$ userC 'pressButton' deviceB` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 11 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'reset' cloudA | deviceB` |
| 12 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'pressButton' deviceB` |
| 13 | `$ userA 'leaves' deviceB` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 14 | `$ userC 'pressButton' deviceB` | `$ userA 'reset' cloudA | deviceB` |
| 15 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 16 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'approach' deviceB` |
| 17 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceB` |
| 18 | `$ userA 'approaches' deviceB` | `$ userA 'reset' cloudA | deviceB` |
| 19 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 20 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `$ userC 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 21 | `$ userC 'callAPI:reset' cloudA` | `$ userC 'reset' cloudA | deviceB` |
| 22 | `` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userC 'leave' deviceB` |
| 25 | `` | `$ userA 'approach' deviceB` |
| 26 | `` | `$ userA 'pressButton' deviceB` |
| 27 | `` | `$ userA 'reset' cloudA | deviceB` |
| 28 | `` | `$ userC 'bind' cloudA | (deviceB ; 'deviceKey')` |
| 29 | `` | `$ userA 'pressButton' deviceB` |
| 30 | `` | `$ userC 'reset' cloudA | deviceB` |
| 31 | `` | `$ userA 'pressButton' deviceB` |
| 32 | `` | `$ userA 'bind' cloudA | (deviceB ; 'deviceKey')` |

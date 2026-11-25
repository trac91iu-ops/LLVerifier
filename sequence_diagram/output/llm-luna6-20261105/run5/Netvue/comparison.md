# Netvue

- input: `sequence_diagram/input/Netvue/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Netvue/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (22 events); golden: counterexample (25 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 2 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'pressButton' deviceB` |
| 4 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'bindDevice' cloudA | (deviceB ; encrypt('Text'2357136044, 'keyB'))` |
| 5 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'resetDevice' cloudA | deviceB` |
| 6 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 7 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userC 'pressButton' deviceB` |
| 8 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'bindDevice' cloudA | (deviceB ; encrypt('Text'2357136044, 'keyB'))` |
| 9 | `$ userA 'approaches' deviceB` | `$ userC 'bindDevice' cloudA | (deviceB ; encrypt('Text'362609376e, 'keyB'))` |
| 10 | `$ userC 'approaches' deviceB` | `$ userA 'resetDevice' cloudA | deviceB` |
| 11 | `$ userC 'pressButton' deviceB` | `$ userC 'resetDevice' cloudA | deviceB` |
| 12 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'leave' deviceB` |
| 13 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userA 'bindDevice' cloudA | (deviceB ; encrypt('Text'2357136044, 'keyB'))` |
| 14 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'bindDevice' cloudA | (deviceB ; encrypt('Text'362609376e, 'keyB'))` |
| 15 | `$ userC 'callAPI:reset' cloudA` | `$ userA 'resetDevice' cloudA | deviceB` |
| 16 | `$ userA 'leaves' deviceB` | `$ userC 'resetDevice' cloudA | deviceB` |
| 17 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'approach' deviceB` |
| 18 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'leave' deviceB` |
| 19 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'bindDevice' cloudA | (deviceB ; encrypt('Text'362609376e, 'keyB'))` |
| 20 | `$ userC 'callAPI:reset' cloudA` | `$ userA 'bindDevice' cloudA | (deviceB ; encrypt('Text'2357136044, 'keyB'))` |
| 21 | `$ userC 'leaves' deviceB` | `$ userA 'resetDevice' cloudA | deviceB` |
| 22 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'resetDevice' cloudA | deviceB` |
| 23 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 24 | `$ userA 'callAPI:reset' cloudA` | `` |
| 25 | `$ userC 'callAPI:reset' cloudA` | `` |

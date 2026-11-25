# Kevo

- input: `sequence_diagram/input/Kevo/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run2/Kevo/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (61 events); golden: counterexample (25 events)
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
| 1 | `$ userA 'pressButton' deviceB` | `$ userC 'approach' deviceB` |
| 2 | `$ userA 'pressButton' deviceB` | `$ userA 'leave' deviceB` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'approach' deviceB` |
| 4 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userC 'leave' deviceB` |
| 5 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'leave' deviceB` |
| 6 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 7 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'pressButton' deviceB` |
| 8 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'approach' deviceB` |
| 9 | `$ userA 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 10 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceB` |
| 11 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 12 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'leave' deviceB` |
| 13 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userA 'approach' deviceB` |
| 14 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'pressButton' deviceB` |
| 15 | `$ userC 'callAPI:reset' cloudA` | `$ userC 'approach' deviceB` |
| 16 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 17 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'approach' deviceB` |
| 18 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'leave' deviceB` |
| 19 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'leave' deviceB` |
| 20 | `$ userC 'callAPI:reset' cloudA` | `$ userA 'approach' deviceB` |
| 21 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceB` |
| 22 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'approach' deviceB` |
| 23 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'leave' deviceB` |
| 24 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'approach' deviceB` |
| 25 | `$ userC 'callAPI:reset' cloudA` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userA 'leave' deviceB` |
| 27 | `` | `$ userA 'approach' deviceB` |
| 28 | `` | `$ userA 'bind' cloudA | (deviceB ; encrypt('R'2357136044, 'keyB'))` |
| 29 | `` | `$ userC 'approach' deviceB` |
| 30 | `` | `$ userA 'leave' deviceB` |
| 31 | `` | `$ userA 'approach' deviceB` |
| 32 | `` | `$ userC 'leave' deviceB` |
| 33 | `` | `$ userA 'leave' deviceB` |
| 34 | `` | `$ userC 'approach' deviceB` |
| 35 | `` | `$ userC 'leave' deviceB` |
| 36 | `` | `$ userA 'reset' cloudA | deviceB` |
| 37 | `` | `$ userC 'approach' deviceB` |
| 38 | `` | `$ userC 'pressButton' deviceB` |
| 39 | `` | `$ userA 'approach' deviceB` |
| 40 | `` | `$ userA 'leave' deviceB` |
| 41 | `` | `$ userC 'leave' deviceB` |
| 42 | `` | `$ userC 'bind' cloudA | (deviceB ; encrypt('R'362609376e, 'keyB'))` |
| 43 | `` | `$ userA 'approach' deviceB` |
| 44 | `` | `$ userC 'approach' deviceB` |
| 45 | `` | `$ userA 'leave' deviceB` |
| 46 | `` | `$ userA 'approach' deviceB` |
| 47 | `` | `$ userC 'leave' deviceB` |
| 48 | `` | `$ userA 'leave' deviceB` |
| 49 | `` | `$ userC 'approach' deviceB` |
| 50 | `` | `$ userC 'leave' deviceB` |
| 51 | `` | `$ userA 'bind' cloudA | (deviceB ; encrypt('R'2357136044, 'keyB'))` |
| 52 | `` | `$ userA 'approach' deviceB` |
| 53 | `` | `$ userC 'approach' deviceB` |
| 54 | `` | `$ userA 'leave' deviceB` |
| 55 | `` | `$ userA 'approach' deviceB` |
| 56 | `` | `$ userC 'leave' deviceB` |
| 57 | `` | `$ userA 'leave' deviceB` |
| 58 | `` | `$ userC 'approach' deviceB` |
| 59 | `` | `$ userC 'leave' deviceB` |
| 60 | `` | `$ userA 'reset' cloudA | deviceB` |
| 61 | `` | `$ userC 'reset' cloudA | deviceB` |

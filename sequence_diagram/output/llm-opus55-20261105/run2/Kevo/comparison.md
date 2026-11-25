# Kevo

- input: `sequence_diagram/input/Kevo/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run2/Kevo/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (61 events); golden: counterexample (25 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < userC | ('near' : deviceA , ..) > |= attackerLocal = true .
eq E @ S < cloudA | (deviceA : ('owners' : (userC , Rest) , ..) , ...) > |= attackerOwner = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `$ userC 'approach' deviceA` |
| 2 | `$ userA 'pressButton' deviceB` | `$ userA 'leave' deviceA` |
| 3 | `$ userA 'pressButton' deviceB` | `$ userA 'approach' deviceA` |
| 4 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userC 'leave' deviceA` |
| 5 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'leave' deviceA` |
| 6 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceA` |
| 7 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'pressButton' deviceA` |
| 8 | `$ userA 'callAPI:reset' cloudA` | `$ userC 'approach' deviceA` |
| 9 | `$ userA 'approaches' deviceB` | `$ userA 'leave' deviceA` |
| 10 | `$ userC 'approaches' deviceB` | `$ userA 'approach' deviceA` |
| 11 | `$ userC 'pressButton' deviceB` | `$ userC 'leave' deviceA` |
| 12 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'leave' deviceA` |
| 13 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userA 'approach' deviceA` |
| 14 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'pressButton' deviceA` |
| 15 | `$ userC 'callAPI:reset' cloudA` | `$ userC 'approach' deviceA` |
| 16 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceA` |
| 17 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'approach' deviceA` |
| 18 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'leave' deviceA` |
| 19 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'leave' deviceA` |
| 20 | `$ userC 'callAPI:reset' cloudA` | `$ userA 'approach' deviceA` |
| 21 | `$ userC 'leaves' deviceB` | `$ userA 'pressButton' deviceA` |
| 22 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `$ userC 'approach' deviceA` |
| 23 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `$ userA 'leave' deviceA` |
| 24 | `$ userA 'callAPI:reset' cloudA` | `$ userA 'approach' deviceA` |
| 25 | `$ userC 'callAPI:reset' cloudA` | `$ userC 'leave' deviceA` |
| 26 | `` | `$ userA 'leave' deviceA` |
| 27 | `` | `$ userA 'approach' deviceA` |
| 28 | `` | `$ userA 'bind' cloudA | encrypt('R'2357136044, 'keyA')` |
| 29 | `` | `$ userC 'approach' deviceA` |
| 30 | `` | `$ userA 'leave' deviceA` |
| 31 | `` | `$ userA 'approach' deviceA` |
| 32 | `` | `$ userC 'leave' deviceA` |
| 33 | `` | `$ userA 'leave' deviceA` |
| 34 | `` | `$ userC 'approach' deviceA` |
| 35 | `` | `$ userC 'leave' deviceA` |
| 36 | `` | `$ userA 'reset' cloudA | deviceA` |
| 37 | `` | `$ userC 'approach' deviceA` |
| 38 | `` | `$ userC 'pressButton' deviceA` |
| 39 | `` | `$ userA 'approach' deviceA` |
| 40 | `` | `$ userA 'leave' deviceA` |
| 41 | `` | `$ userC 'leave' deviceA` |
| 42 | `` | `$ userC 'bind' cloudA | encrypt('R'362609376e, 'keyA')` |
| 43 | `` | `$ userA 'approach' deviceA` |
| 44 | `` | `$ userC 'approach' deviceA` |
| 45 | `` | `$ userA 'leave' deviceA` |
| 46 | `` | `$ userA 'approach' deviceA` |
| 47 | `` | `$ userC 'leave' deviceA` |
| 48 | `` | `$ userA 'leave' deviceA` |
| 49 | `` | `$ userC 'approach' deviceA` |
| 50 | `` | `$ userC 'leave' deviceA` |
| 51 | `` | `$ userA 'bind' cloudA | encrypt('R'2357136044, 'keyA')` |
| 52 | `` | `$ userA 'approach' deviceA` |
| 53 | `` | `$ userC 'approach' deviceA` |
| 54 | `` | `$ userA 'leave' deviceA` |
| 55 | `` | `$ userA 'approach' deviceA` |
| 56 | `` | `$ userC 'leave' deviceA` |
| 57 | `` | `$ userA 'leave' deviceA` |
| 58 | `` | `$ userC 'approach' deviceA` |
| 59 | `` | `$ userC 'leave' deviceA` |
| 60 | `` | `$ userA 'reset' cloudA | deviceA` |
| 61 | `` | `$ userC 'reset' cloudA | deviceA` |

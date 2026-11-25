# Broadlink

- input: `sequence_diagram/input/Broadlink/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run2/Broadlink/`
- property: OWN-remote (attacker userC)
- status: validated; verdict: counterexample (88 events); golden: counterexample (21 events)
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
| 4 | `$ userA 'pressButton' deviceB` | `$ userC 'leave' deviceB` |
| 5 | `$ userA 'callAPI:getKey' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'approach' deviceB` |
| 7 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'pressButton' deviceB` |
| 8 | `$ userA 'leaves' deviceB` | `$ userC 'approach' deviceB` |
| 9 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userA 'leave' deviceB` |
| 10 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'approach' deviceB` |
| 11 | `$ userA 'approaches' deviceB` | `$ userC 'leave' deviceB` |
| 12 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 13 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'approach' deviceB` |
| 14 | `$ userA 'callAPI:lock' deviceB | 'KeyB'362609376e` | `$ userA 'pressButton' deviceB` |
| 15 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'approach' deviceB` |
| 16 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'leave' deviceB` |
| 17 | `$ userA 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 18 | `$ userC 'callAPI:invite' cloudA | userA` | `$ userC 'leave' deviceB` |
| 19 | `$ userC 'callAPI:kick' cloudA | userA` | `$ userA 'leave' deviceB` |
| 20 | `$ userC 'leaves' deviceB` | `$ userA 'approach' deviceB` |
| 21 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'KeyB'362609376e)` | `$ userA 'pressButton' deviceB` |
| 22 | `` | `$ userC 'approach' deviceB` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userA 'approach' deviceB` |
| 25 | `` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userA 'leave' deviceB` |
| 27 | `` | `$ userA 'approach' deviceB` |
| 28 | `` | `$ userA 'pressButton' deviceB` |
| 29 | `` | `$ userC 'approach' deviceB` |
| 30 | `` | `$ userA 'leave' deviceB` |
| 31 | `` | `$ userA 'approach' deviceB` |
| 32 | `` | `$ userC 'leave' deviceB` |
| 33 | `` | `$ userA 'leave' deviceB` |
| 34 | `` | `$ userA 'approach' deviceB` |
| 35 | `` | `$ userA 'retrieveKey' deviceB` |
| 36 | `` | `$ userC 'approach' deviceB` |
| 37 | `` | `$ userA 'leave' deviceB` |
| 38 | `` | `$ userA 'approach' deviceB` |
| 39 | `` | `$ userC 'leave' deviceB` |
| 40 | `` | `$ userA 'leave' deviceB` |
| 41 | `` | `$ userA 'approach' deviceB` |
| 42 | `` | `$ userA 'bind' cloudA | (deviceB ; 'KeyA'362609376e)` |
| 43 | `` | `$ userC 'approach' deviceB` |
| 44 | `` | `$ userA 'leave' deviceB` |
| 45 | `` | `$ userA 'approach' deviceB` |
| 46 | `` | `$ userC 'leave' deviceB` |
| 47 | `` | `$ userA 'leave' deviceB` |
| 48 | `` | `$ userA 'approach' deviceB` |
| 49 | `` | `$ userC 'invite' cloudA | userA` |
| 50 | `` | `$ userC 'approach' deviceB` |
| 51 | `` | `$ userA 'leave' deviceB` |
| 52 | `` | `$ userA 'approach' deviceB` |
| 53 | `` | `$ userC 'leave' deviceB` |
| 54 | `` | `$ userA 'leave' deviceB` |
| 55 | `` | `$ userA 'approach' deviceB` |
| 56 | `` | `$ userC 'remove' cloudA | userA` |
| 57 | `` | `$ userC 'approach' deviceB` |
| 58 | `` | `$ userA 'leave' deviceB` |
| 59 | `` | `$ userA 'approach' deviceB` |
| 60 | `` | `$ userC 'leave' deviceB` |
| 61 | `` | `$ userA 'leave' deviceB` |
| 62 | `` | `$ userC 'approach' deviceB` |
| 63 | `` | `$ userC 'leave' deviceB` |
| 64 | `` | `$ userC 'invite' cloudA | userA` |
| 65 | `` | `$ userC 'approach' deviceB` |
| 66 | `` | `$ userC 'retrieveKey' deviceB` |
| 67 | `` | `$ userA 'approach' deviceB` |
| 68 | `` | `$ userA 'leave' deviceB` |
| 69 | `` | `$ userC 'leave' deviceB` |
| 70 | `` | `$ userC 'bind' cloudA | (deviceB ; 'KeyA'362609376e)` |
| 71 | `` | `$ userA 'approach' deviceB` |
| 72 | `` | `$ userC 'approach' deviceB` |
| 73 | `` | `$ userA 'leave' deviceB` |
| 74 | `` | `$ userA 'approach' deviceB` |
| 75 | `` | `$ userC 'leave' deviceB` |
| 76 | `` | `$ userA 'leave' deviceB` |
| 77 | `` | `$ userC 'approach' deviceB` |
| 78 | `` | `$ userC 'leave' deviceB` |
| 79 | `` | `$ userC 'invite' cloudA | userA` |
| 80 | `` | `$ userA 'approach' deviceB` |
| 81 | `` | `$ userC 'approach' deviceB` |
| 82 | `` | `$ userA 'leave' deviceB` |
| 83 | `` | `$ userA 'approach' deviceB` |
| 84 | `` | `$ userC 'leave' deviceB` |
| 85 | `` | `$ userA 'leave' deviceB` |
| 86 | `` | `$ userC 'approach' deviceB` |
| 87 | `` | `$ userC 'leave' deviceB` |
| 88 | `` | `$ userC 'remove' cloudA | userA` |

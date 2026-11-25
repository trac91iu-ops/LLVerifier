# MaagKwikset

- input: `sequence_diagram/input/MaagKwikset/diagram.md`
- output: `sequence_diagram/output/llm-opus55-20261105/run5/MaagKwikset/`
- property: OWN-stealth (attacker userC)
- status: validated; verdict: counterexample (69 events); golden: counterexample (14 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceA | ('trusted' : (userC , Rest) , ..) > |= deviceTrustsAttacker = true .
eq E @ S < cloudA | (deviceA : ('trusted' : (userC , Rest) , ..) , ...) > |= cloudRecordsTrust = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'approach' deviceA` |
| 2 | `$ userA 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2357136044)` | `$ userA 'leave' deviceA` |
| 3 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userA 'approach' deviceA` |
| 4 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userC 'leave' deviceA` |
| 5 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceA` |
| 6 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userA 'approach' deviceA` |
| 7 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userA 'requestKey' deviceA` |
| 8 | `$ userA 'approaches' deviceB` | `$ userC 'approach' deviceA` |
| 9 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceA` |
| 10 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'approach' deviceA` |
| 11 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userC 'leave' deviceA` |
| 12 | `$ userC 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2546248239)` | `$ userA 'leave' deviceA` |
| 13 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userA 'approach' deviceA` |
| 14 | `$ userC 'callAPI:bind' deviceB | encrypt('secret', 'KeyA'2546248239)` | `$ userA 'signKey' cloudA | (deviceA ; 'Key'2357136044)` |
| 15 | `` | `$ userC 'approach' deviceA` |
| 16 | `` | `$ userA 'leave' deviceA` |
| 17 | `` | `$ userA 'approach' deviceA` |
| 18 | `` | `$ userC 'leave' deviceA` |
| 19 | `` | `$ userA 'leave' deviceA` |
| 20 | `` | `$ userA 'approach' deviceA` |
| 21 | `` | `$ userA 'share' cloudA | (deviceA ; userC)` |
| 22 | `` | `$ userC 'approach' deviceA` |
| 23 | `` | `$ userA 'leave' deviceA` |
| 24 | `` | `$ userA 'approach' deviceA` |
| 25 | `` | `$ userC 'leave' deviceA` |
| 26 | `` | `$ userA 'leave' deviceA` |
| 27 | `` | `$ userA 'approach' deviceA` |
| 28 | `` | `$ userC 'revoke' cloudA | (deviceA ; userA)` |
| 29 | `` | `$ userC 'approach' deviceA` |
| 30 | `` | `$ userA 'leave' deviceA` |
| 31 | `` | `$ userA 'approach' deviceA` |
| 32 | `` | `$ userC 'leave' deviceA` |
| 33 | `` | `$ userA 'leave' deviceA` |
| 34 | `` | `$ userC 'approach' deviceA` |
| 35 | `` | `$ userC 'leave' deviceA` |
| 36 | `` | `$ userC 'share' cloudA | (deviceA ; userA)` |
| 37 | `` | `$ userC 'approach' deviceA` |
| 38 | `` | `$ userC 'leave' deviceA` |
| 39 | `` | `$ userA 'revoke' cloudA | (deviceA ; userC)` |
| 40 | `` | `$ userC 'approach' deviceA` |
| 41 | `` | `$ userC 'requestKey' deviceA` |
| 42 | `` | `$ userA 'approach' deviceA` |
| 43 | `` | `$ userA 'leave' deviceA` |
| 44 | `` | `$ userC 'leave' deviceA` |
| 45 | `` | `$ userA 'approach' deviceA` |
| 46 | `` | `$ userC 'approach' deviceA` |
| 47 | `` | `$ userC 'leave' deviceA` |
| 48 | `` | `$ userA 'leave' deviceA` |
| 49 | `` | `$ userC 'approach' deviceA` |
| 50 | `` | `$ userA 'share' cloudA | (deviceA ; userC)` |
| 51 | `` | `$ userA 'approach' deviceA` |
| 52 | `` | `$ userA 'leave' deviceA` |
| 53 | `` | `$ userC 'leave' deviceA` |
| 54 | `` | `$ userA 'approach' deviceA` |
| 55 | `` | `$ userC 'approach' deviceA` |
| 56 | `` | `$ userC 'leave' deviceA` |
| 57 | `` | `$ userA 'leave' deviceA` |
| 58 | `` | `$ userC 'approach' deviceA` |
| 59 | `` | `$ userC 'signKey' cloudA | (deviceA ; 'Key'2546248239)` |
| 60 | `` | `$ userA 'approach' deviceA` |
| 61 | `` | `$ userA 'leave' deviceA` |
| 62 | `` | `$ userC 'leave' deviceA` |
| 63 | `` | `$ userA 'approach' deviceA` |
| 64 | `` | `$ userC 'approach' deviceA` |
| 65 | `` | `$ userC 'leave' deviceA` |
| 66 | `` | `$ userA 'leave' deviceA` |
| 67 | `` | `$ userC 'approach' deviceA` |
| 68 | `` | `$ userA 'revoke' cloudA | (deviceA ; userC)` |
| 69 | `` | `$ userC 'bind' deviceA | encrypt('Key'2546248239, 'secret')` |

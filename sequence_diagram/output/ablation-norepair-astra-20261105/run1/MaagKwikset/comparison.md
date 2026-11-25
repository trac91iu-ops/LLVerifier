# MaagKwikset

- input: `sequence_diagram/input/MaagKwikset/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run1/MaagKwikset/`
- property: OWN-stealth (attacker userC)
- status: validated; verdict: counterexample (69 events); golden: counterexample (14 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('trustedUsers' : (userC , Rest) , ..) > |= deviceTrustsAttacker = true .
eq E @ S < cloudA | (deviceB : ('trustedUsers' : (userC , Rest) , ..) , ...) > |= cloudRecordsTrust = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' deviceB` | `$ userC 'approach' deviceB` |
| 2 | `$ userA 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2357136044)` | `$ userA 'leave' deviceB` |
| 3 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userA 'approach' deviceB` |
| 4 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userC 'leave' deviceB` |
| 5 | `$ userA 'leaves' deviceB` | `$ userA 'leave' deviceB` |
| 6 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userA 'approach' deviceB` |
| 7 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userA 'requestKey' deviceB` |
| 8 | `$ userA 'approaches' deviceB` | `$ userC 'approach' deviceB` |
| 9 | `$ userC 'approaches' deviceB` | `$ userA 'leave' deviceB` |
| 10 | `$ userC 'callAPI:getKey' deviceB` | `$ userA 'approach' deviceB` |
| 11 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `$ userC 'leave' deviceB` |
| 12 | `$ userC 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2546248239)` | `$ userA 'leave' deviceB` |
| 13 | `$ userA 'callAPI:revoke' cloudA | userC` | `$ userA 'approach' deviceB` |
| 14 | `$ userC 'callAPI:bind' deviceB | encrypt('secret', 'KeyA'2546248239)` | `$ userA 'signKey' cloudA | (deviceB ; 'Key'2357136044)` |
| 15 | `` | `$ userC 'approach' deviceB` |
| 16 | `` | `$ userA 'leave' deviceB` |
| 17 | `` | `$ userA 'approach' deviceB` |
| 18 | `` | `$ userC 'leave' deviceB` |
| 19 | `` | `$ userA 'leave' deviceB` |
| 20 | `` | `$ userA 'approach' deviceB` |
| 21 | `` | `$ userA 'shareAccess' cloudA | (deviceB ; userC)` |
| 22 | `` | `$ userC 'approach' deviceB` |
| 23 | `` | `$ userA 'leave' deviceB` |
| 24 | `` | `$ userA 'approach' deviceB` |
| 25 | `` | `$ userC 'leave' deviceB` |
| 26 | `` | `$ userA 'leave' deviceB` |
| 27 | `` | `$ userA 'approach' deviceB` |
| 28 | `` | `$ userC 'revokeAccess' cloudA | (deviceB ; userA)` |
| 29 | `` | `$ userC 'approach' deviceB` |
| 30 | `` | `$ userA 'leave' deviceB` |
| 31 | `` | `$ userA 'approach' deviceB` |
| 32 | `` | `$ userC 'leave' deviceB` |
| 33 | `` | `$ userA 'leave' deviceB` |
| 34 | `` | `$ userC 'approach' deviceB` |
| 35 | `` | `$ userC 'leave' deviceB` |
| 36 | `` | `$ userC 'shareAccess' cloudA | (deviceB ; userA)` |
| 37 | `` | `$ userC 'approach' deviceB` |
| 38 | `` | `$ userC 'leave' deviceB` |
| 39 | `` | `$ userA 'revokeAccess' cloudA | (deviceB ; userC)` |
| 40 | `` | `$ userC 'approach' deviceB` |
| 41 | `` | `$ userC 'requestKey' deviceB` |
| 42 | `` | `$ userA 'approach' deviceB` |
| 43 | `` | `$ userA 'leave' deviceB` |
| 44 | `` | `$ userC 'leave' deviceB` |
| 45 | `` | `$ userA 'approach' deviceB` |
| 46 | `` | `$ userC 'approach' deviceB` |
| 47 | `` | `$ userC 'leave' deviceB` |
| 48 | `` | `$ userA 'leave' deviceB` |
| 49 | `` | `$ userC 'approach' deviceB` |
| 50 | `` | `$ userA 'shareAccess' cloudA | (deviceB ; userC)` |
| 51 | `` | `$ userA 'approach' deviceB` |
| 52 | `` | `$ userA 'leave' deviceB` |
| 53 | `` | `$ userC 'leave' deviceB` |
| 54 | `` | `$ userA 'approach' deviceB` |
| 55 | `` | `$ userC 'approach' deviceB` |
| 56 | `` | `$ userC 'leave' deviceB` |
| 57 | `` | `$ userA 'leave' deviceB` |
| 58 | `` | `$ userC 'approach' deviceB` |
| 59 | `` | `$ userC 'signKey' cloudA | (deviceB ; 'Key'2546248239)` |
| 60 | `` | `$ userA 'approach' deviceB` |
| 61 | `` | `$ userA 'leave' deviceB` |
| 62 | `` | `$ userC 'leave' deviceB` |
| 63 | `` | `$ userA 'approach' deviceB` |
| 64 | `` | `$ userC 'approach' deviceB` |
| 65 | `` | `$ userC 'leave' deviceB` |
| 66 | `` | `$ userA 'leave' deviceB` |
| 67 | `` | `$ userC 'approach' deviceB` |
| 68 | `` | `$ userA 'revokeAccess' cloudA | (deviceB ; userC)` |
| 69 | `` | `$ userC 'bind' deviceB | encrypt('Key'2546248239, 'secret')` |

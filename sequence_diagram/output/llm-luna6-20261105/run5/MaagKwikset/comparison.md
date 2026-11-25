# MaagKwikset

- input: `sequence_diagram/input/MaagKwikset/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/MaagKwikset/`
- property: OWN-stealth (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (14 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('trusted' : (userC , Rest) , ..) > |= deviceTrustsAttacker = true .
eq E @ S < cloudA | (deviceB : ('trusted' : (userC , Rest) , ..) , ...) > |= cloudRecordsTrust = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 2 | `$ userA 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2357136044)` | `` |
| 3 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `` |
| 4 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 5 | `$ userA 'leaves' deviceB` | `` |
| 6 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `` |
| 7 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 8 | `$ userA 'approaches' deviceB` | `` |
| 9 | `$ userC 'approaches' deviceB` | `` |
| 10 | `$ userC 'callAPI:getKey' deviceB` | `` |
| 11 | `$ userA 'callAPI:share' cloudA | (userC ; deviceB)` | `` |
| 12 | `$ userC 'callAPI:signKey' cloudA | (deviceB ; 'KeyA'2546248239)` | `` |
| 13 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 14 | `$ userC 'callAPI:bind' deviceB | encrypt('secret', 'KeyA'2546248239)` | `` |

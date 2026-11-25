# MaagLevel

- input: `sequence_diagram/input/MaagLevel/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run4/MaagLevel/`
- property: OWN-stealth (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (23 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < deviceB | ('trusted' : (userC , Rest) , ..) > |= deviceTrustsAttacker = true .
eq E @ S < cloudB | (deviceB : ('trusted' : (userC , Rest) , ..) , ...) > |= cloudRecordsTrust = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'approaches' deviceB` | `` |
| 2 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 3 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 4 | `$ userA 'leaves' deviceB` | `` |
| 5 | `$ userC 'approaches' deviceB` | `` |
| 6 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 7 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 8 | `$ userC 'callAPI:proxy' deviceB | (encrypt('secret', 'auth') ; 'share' ; userC)` | `` |
| 9 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 10 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 11 | `$ userC 'leaves' deviceB` | `` |
| 12 | `$ userA 'approaches' deviceB` | `` |
| 13 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 14 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 15 | `$ userA 'leaves' deviceB` | `` |
| 16 | `$ userA 'approaches' deviceB` | `` |
| 17 | `$ userC 'approaches' deviceB` | `` |
| 18 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 19 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 20 | `$ userC 'callAPI:proxy' deviceB | (encrypt('secret', 'auth') ; 'share' ; userC)` | `` |
| 21 | `$ userA 'callAPI:share' cloudA | userC` | `` |
| 22 | `$ userA 'callAPI:revoke' cloudA | userC` | `` |
| 23 | `$ userA 'leaves' deviceB` | `` |

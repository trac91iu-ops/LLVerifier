# Kevo

- input: `sequence_diagram/input/Kevo/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run2/Kevo/`
- property: OWN-remote (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (25 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < UserX | 'near' : OldNear , ... > $ UserX 'approach' deviceB
=> < UserX | 'near

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'pressButton' deviceB` | `` |
| 3 | `$ userA 'pressButton' deviceB` | `` |
| 4 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 5 | `$ userA 'callAPI:reset' cloudA` | `` |
| 6 | `$ userA 'leaves' deviceB` | `` |
| 7 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 8 | `$ userA 'callAPI:reset' cloudA` | `` |
| 9 | `$ userA 'approaches' deviceB` | `` |
| 10 | `$ userC 'approaches' deviceB` | `` |
| 11 | `$ userC 'pressButton' deviceB` | `` |
| 12 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 13 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `` |
| 14 | `$ userA 'callAPI:reset' cloudA` | `` |
| 15 | `$ userC 'callAPI:reset' cloudA` | `` |
| 16 | `$ userA 'leaves' deviceB` | `` |
| 17 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 18 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `` |
| 19 | `$ userA 'callAPI:reset' cloudA` | `` |
| 20 | `$ userC 'callAPI:reset' cloudA` | `` |
| 21 | `$ userC 'leaves' deviceB` | `` |
| 22 | `$ userC 'callAPI:bind' cloudA | encrypt('RandomString'362609376e, 'secret')` | `` |
| 23 | `$ userA 'callAPI:bind' cloudA | encrypt('RandomString'2357136044, 'secret')` | `` |
| 24 | `$ userA 'callAPI:reset' cloudA` | `` |
| 25 | `$ userC 'callAPI:reset' cloudA` | `` |

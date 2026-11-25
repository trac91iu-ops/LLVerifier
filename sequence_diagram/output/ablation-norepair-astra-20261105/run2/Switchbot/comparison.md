# Switchbot

- input: `sequence_diagram/input/Switchbot/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run2/Switchbot/`
- property: OWN-remote (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (33 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 0 repairs: Every rule must start with its block label such as `[B1]`; found unlabeled text: < deviceB | 'key' : Key , ... > $ UserX 'pressButton' deviceB
=> < deviceB | 'ke

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `` |
| 3 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 4 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 5 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 6 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 7 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 8 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 9 | `$ userA 'leaves' deviceB` | `` |
| 10 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 11 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 12 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 13 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 14 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 15 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 16 | `$ userA 'approaches' deviceB` | `` |
| 17 | `$ userC 'approaches' deviceB` | `` |
| 18 | `$ userC 'pressButton' deviceB` | `` |
| 19 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 20 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 21 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 22 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 23 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 24 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 25 | `$ userA 'leaves' deviceB` | `` |
| 26 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 27 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 28 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 29 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 30 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 31 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 32 | `$ userC 'leaves' deviceB` | `` |
| 33 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'secret')` | `` |

# Broadlink

- input: `sequence_diagram/input/Broadlink/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/Broadlink/`
- property: OWN-remote (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (21 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Expected exactly one complete output code block.

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'pressButton' deviceB` | `` |
| 2 | `$ userA 'pressButton' deviceB` | `` |
| 3 | `$ userA 'pressButton' deviceB` | `` |
| 4 | `$ userA 'pressButton' deviceB` | `` |
| 5 | `$ userA 'callAPI:getKey' deviceB` | `` |
| 6 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 7 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 8 | `$ userA 'leaves' deviceB` | `` |
| 9 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 10 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 11 | `$ userA 'approaches' deviceB` | `` |
| 12 | `$ userC 'approaches' deviceB` | `` |
| 13 | `$ userC 'callAPI:getKey' deviceB` | `` |
| 14 | `$ userA 'callAPI:lock' deviceB | 'KeyB'362609376e` | `` |
| 15 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 16 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 17 | `$ userA 'leaves' deviceB` | `` |
| 18 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 19 | `$ userC 'callAPI:kick' cloudA | userA` | `` |
| 20 | `$ userC 'leaves' deviceB` | `` |
| 21 | `$ userC 'callAPI:bind' cloudA | (deviceB ; 'KeyB'362609376e)` | `` |

# TuyaCAC

- input: `sequence_diagram/input/TuyaCAC/diagram.md`
- output: `sequence_diagram/output/llm-luna6-20261105/run5/TuyaCAC/`
- property: CTRL-direct (attacker userC)
- status: failed; verdict: None (0 events); golden: counterexample (6 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 2 repairs: No terminal matches '.' in the current parser context, at line 1 col 24

< userA | ... > => ev1 .
                       ^
Expected one of: '\\('

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudA | deviceB` | `` |
| 2 | `$ userA 'callAPI:invite' cloudA | userC` | `` |
| 3 | `$ userC 'callAPI:getKey' cloudA | deviceB` | `` |
| 4 | `$ userC 'callAPI:invite' cloudA | userA` | `` |
| 5 | `$ userA 'callAPI:kick' cloudA | userC` | `` |
| 6 | `$ userC 'callAPI:toggle' deviceB | 'secret'` | `` |

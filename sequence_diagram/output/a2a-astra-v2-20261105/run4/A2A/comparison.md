# A2A

- input: `sequence_diagram/input/A2A/diagram.md`
- output: `sequence_diagram/output/a2a-astra-v2-20261105/run4/A2A/`
- property: CTX-isolation (attacker clientB)
- status: failed; verdict: None (0 events); golden: counterexample (4 events)
- slots false at init expected; true at init: None
- coverage issues: None
- error: ValueError: Validation failed after 2 repairs: Expected nonempty DSL rules.

## Generated slots
```
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ clientA 'SendMessage' serverA | ('contextId' : nils ; 'payload' : 'msgA')` | `` |
| 2 | `$ clientB 'snoopContext' serverA | ('contextId' : 'ctxX')` | `` |
| 3 | `$ clientB 'SendMessage' serverA | ('contextId' : 'ctxX' ; 'payload' : 'msgB')` | `` |
| 4 | `$ clientA 'SendMessage' serverA | ('contextId' : 'ctxX' ; 'payload' : 'msgA2')` | `` |

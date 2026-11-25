# A2A

- input: `sequence_diagram/input/A2A/diagram.md`
- output: `sequence_diagram/output/a2a-astra-v2-20261105/run1/A2A/`
- property: CTX-isolation (attacker clientB)
- status: validated; verdict: counterexample (6 events); golden: counterexample (4 events)
- slots false at init expected; true at init: []
- coverage issues: []

## Generated slots
```
eq E @ S < clientB | ('receivedHistory' : ('msgA' , Rest) , ..) > |= attackerReadsVictimData = true .
eq E @ S < serverA | ('context' : 'ctxX' , 'history' : ('msgB' , Rest) , ..) > |= victimContextTampered = true .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ clientA 'SendMessage' serverA | ('contextId' : nils ; 'payload' : 'msgA')` | `$ clientA 'sendWithoutContext' serverA | 'msgA'` |
| 2 | `$ clientB 'snoopContext' serverA | ('contextId' : 'ctxX')` | `$ clientB 'snoop' serverA | 'ctxX'` |
| 3 | `$ clientB 'SendMessage' serverA | ('contextId' : 'ctxX' ; 'payload' : 'msgB')` | `$ clientA 'sendWithContext' serverA | ('ctxX' ; 'msgB')` |
| 4 | `$ clientA 'SendMessage' serverA | ('contextId' : 'ctxX' ; 'payload' : 'msgA2')` | `$ clientB 'sendWithContext' serverA | ('ctxX' ; 'msgB')` |
| 5 | `` | `$ clientA 'sendWithContext' serverA | ('ctxX' ; 'msgA2')` |
| 6 | `` | `$ clientB 'sendWithContext' serverA | ('ctxX' ; 'msgB')` |

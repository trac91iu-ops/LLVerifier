# delegationFlaw2

- input: `sequence_diagram/input/delegationFlaw2/diagram.md`
- output: `sequence_diagram/output/ablation-norepair-astra-20261105/run5/delegationFlaw2/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: counterexample (5 events); golden: counterexample (5 events)
- slots false at init expected; true at init: []
- coverage issues: ['B6 (action, line 50): no event rule for the initiated message', 'B7 (action, line 55): no event rule for the initiated message']

## Generated slots
```
eq E @ S < deviceLock | ('on' : true , ..) > |= deviceOn = true .
eq E @ S < cloudB | (deviceLock : ('trusted' : (userC , Rest) , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudSmartThing` | `$ userA 'requestKey' cloudSmartThing` |
| 2 | `$ userA 'callAPI:delegate' cloudSmartThing | (userC ; deviceSwitch)` | `$ userA 'delegateAccess' cloudSmartThing | (deviceSwitch ; userC)` |
| 3 | `$ userC 'callAPI:getKey' cloudSmartThing` | `$ userC 'requestKey' cloudSmartThing` |
| 4 | `$ userA 'callAPI:revoke' cloudSmartThing | (userC ; deviceSwitch)` | `$ userC 'turnOnWithKey' cloudSmartThing | (deviceSwitch ; 'key')` |
| 5 | `$ userC 'callAPI:cloudAPI:toggle' cloudSmartThing | (deviceSwitch ; 'secret')` | `$ userA 'revokeAccess' cloudSmartThing | (deviceSwitch ; userC)` |

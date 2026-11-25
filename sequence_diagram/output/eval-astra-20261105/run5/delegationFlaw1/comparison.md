# delegationFlaw1

- input: `sequence_diagram/input/delegationFlaw1/diagram.md`
- output: `sequence_diagram/output/eval-astra-20261105/run5/delegationFlaw1/`
- property: CTRL-direct (attacker userC)
- status: validated; verdict: holds (0 events); golden: counterexample (20 events)
- slots false at init expected; true at init: []
- coverage issues: ['B6 (action, line 49): no event rule for the initiated message', 'B7 (action, line 54): no event rule for the initiated message']

## Generated slots
```
eq E @ S < cloudGoogle | (deviceSwitch : ('on' : true , ..) , ...) > |= deviceOn = true .
eq E @ S < cloudGoogle | (deviceSwitch : ('trusted' : (userC , Rest) , ..) , ...) > |= attackerAuthorized = true .
ceq E @ S |= attackerActs = true if subject(E) == userC .
```

## Counterexamples

| # | golden | generated |
|---|---|---|
| 1 | `$ userA 'callAPI:getKey' cloudGoogle` | `` |
| 2 | `$ userA 'callAPI:delegate' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 3 | `$ userC 'callAPI:getKey' cloudGoogle` | `` |
| 4 | `$ userA 'callAPI:revoke' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 5 | `$ userA 'callAPI:provide' cloudSmartThing | (deviceSwitch ; 'secret')` | `` |
| 6 | `$ userA 'callAPI:delegate' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 7 | `$ userA 'callAPI:delegate' cloudSmartThing | (userC ; deviceSwitch)` | `` |
| 8 | `$ userA 'callAPI:revoke' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 9 | `$ userC 'callAPI:toggle' deviceSwitch` | `` |
| 10 | `$ userA 'callAPI:delegate' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 11 | `$ userA 'callAPI:revoke' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 12 | `$ userA 'callAPI:revoke' cloudSmartThing | (userC ; deviceSwitch)` | `` |
| 13 | `$ userA 'callAPI:delegate' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 14 | `$ userA 'callAPI:revoke' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 15 | `$ userC 'callAPI:provide' cloudSmartThing | (deviceSwitch ; 'secret')` | `` |
| 16 | `$ userC 'callAPI:revoke' cloudSmartThing | (userA ; deviceSwitch)` | `` |
| 17 | `$ userA 'callAPI:delegate' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 18 | `$ userA 'callAPI:revoke' cloudGoogle | (userC ; deviceSwitch)` | `` |
| 19 | `$ userA 'callAPI:provide' cloudSmartThing | (deviceSwitch ; 'secret')` | `` |
| 20 | `$ userA 'callAPI:toggle' deviceSwitch` | `` |

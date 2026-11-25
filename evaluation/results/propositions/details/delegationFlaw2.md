# delegationFlaw2: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## deviceOn: literal (run1, run2, run3, run4, run5)

- gold: `< deviceLock | ('state' : true , ..) >`
- generated: `< deviceLock | ('on' : true , ..) >`
- renamed: `< deviceLock | ( 'state' : true , .. ) >`
- precise True, recalled True

## attackerAuthorized: different (run1, run2, run3, run4, run5)

- gold: `< cloudSmartThing | (deviceSwitch : ('trustSet' : (userC, ....) , ..) , ...) >`
- generated: `< cloudB | (deviceLock : ('trusted' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudB | ( deviceLock : ( 'trustSet' : ( userC , RestG ) , .. ) , ... ) >`
- precise False, recalled False

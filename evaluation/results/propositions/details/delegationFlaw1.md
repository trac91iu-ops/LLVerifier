# delegationFlaw1: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## deviceOn: generated narrower (run1, run2, run3, run4, run5)

- gold: `< deviceLock | ('state' : true , ..) >`
- generated: `< cloudGoogle | (deviceSwitch : ('on' : true , ..) , ...) >`
- renamed: `< cloudGoogle | ( deviceSwitch : ( 'state' : true , .. ) , ... ) >`
- precise True, recalled False

## attackerAuthorized: same meaning (run1, run2, run3, run4, run5)

- gold: `< cloudGoogle | (deviceSwitch : ('trust' : (userC, ..) , ...) , ....) >`
- generated: `< cloudGoogle | (deviceSwitch : ('trusted' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudGoogle | ( deviceSwitch : ( 'trust' : ( userC , RestG ) , .. ) , ... ) >`
- precise True, recalled True

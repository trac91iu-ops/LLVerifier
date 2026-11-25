# Broadlink: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## attackerLocal: not generated (run1, run2, run4)

- gold: `< userC | ('localTo' : deviceB , ..) >`
- generated: `None`
- renamed: `None`
- precise False, recalled False; error: not generated

## attackerOwner: not generated (run1, run2, run4)

- gold: `< cloudA | (deviceB : ('owner' : userC , ..) , ...) >`
- generated: `None`
- renamed: `None`
- precise False, recalled False; error: not generated

## attackerLocal: literal (run3, run5)

- gold: `< userC | ('localTo' : deviceB , ..) >`
- generated: `< userC | ('near' : deviceB , ..) >`
- renamed: `< userC | ( 'localTo' : deviceB , .. ) >`
- precise True, recalled True

## attackerOwner: generated wider (run3, run5)

- gold: `< cloudA | (deviceB : ('owner' : userC , ..) , ...) >`
- generated: `< cloudA | (deviceB : ('owners' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudA | ( deviceB : ( 'owner' : ( userC , RestG ) , .. ) , ... ) >`
- precise False, recalled True

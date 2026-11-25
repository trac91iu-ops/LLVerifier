# Kevo: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## attackerLocal: generated wider (run1, run2, run3, run4, run5)

- gold: `< userC | ('message' : QidA , 'localTo' : deviceB , ..) >`
- generated: `< userC | ('near' : deviceB , ..) >`
- renamed: `< userC | ( 'localTo' : deviceB , .. ) >`
- precise False, recalled True

## attackerOwner: literal (run1, run2, run3, run5)

- gold: `< cloudA | (deviceB : ('owner' : userC , ..) , ...) >`
- generated: `< cloudA | (deviceB : ('owners' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudA | ( deviceB : ( 'owner' : userC , .. ) , ... ) >`
- precise True, recalled True

## attackerOwner: same meaning (run4)

- gold: `< cloudA | (deviceB : ('owner' : userC , ..) , ...) >`
- generated: `< cloudA | (deviceB : ('owners' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudA | ( deviceB : ( 'owner' : ( userC , RestG ) , .. ) , ... ) >`
- precise True, recalled True

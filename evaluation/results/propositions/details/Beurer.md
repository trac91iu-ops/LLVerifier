# Beurer: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## attackerLocal: literal (run1, run2, run3, run4, run5)

- gold: `< userC | ('localTo' : deviceB , ..) >`
- generated: `< userC | ('near' : deviceB , ..) >`
- renamed: `< userC | ( 'localTo' : deviceB , .. ) >`
- precise True, recalled True

## attackerOwner: same meaning (run1, run2, run3, run4, run5)

- gold: `< cloudA | (deviceB : ('key' : KeyA , 'owner' : userC , ..) , ...) >`
- generated: `< cloudA | (deviceB : ('owner' : userC , ..) , ...) >`
- renamed: `< cloudA | ( deviceB : ( 'owner' : userC , .. ) , ... ) >`
- precise True, recalled True

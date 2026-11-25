# MaagLevel: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## deviceTrustsAttacker: same meaning (run1, run2, run3, run4, run5)

- gold: `< deviceB | ('trustSet' : (userC , ..) , ...) >`
- generated: `< deviceB | ('trusted' : (userC , Rest) , ..) >`
- renamed: `< deviceB | ( 'trustSet' : ( userC , RestG ) , .. ) >`
- precise True, recalled True

## cloudRecordsTrust: same meaning (run1, run2, run3, run4, run5)

- gold: `< cloudA | (deviceB : ('trustSet' : (userC , ....) , ..) , ...) >`
- generated: `< cloudA | (deviceB : ('trusted' : (userC , Rest) , ..) , ...) >`
- renamed: `< cloudA | ( deviceB : ( 'trustSet' : ( userC , RestG ) , .. ) , ... ) >`
- precise True, recalled True

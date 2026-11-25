# Huawei: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## deviceOn: literal (run1, run2, run3, run4, run5)

- gold: `< deviceB | ('state' : 'on' , ..) >`
- generated: `< deviceB | ('on' : true , ..) >`
- renamed: `< deviceB | ( 'state' : 'on' , .. ) >`
- precise True, recalled True

## attackerAuthorized: literal (run1, run2, run3, run4, run5)

- gold: `< cloudA | (userC : ('device' : deviceB , ..) , ...) >`
- generated: `< cloudA | (userC : ('device' : deviceB , ..) , ...) >`
- renamed: `< cloudA | ( userC : ( 'device' : deviceB , .. ) , ... ) >`
- precise True, recalled True

# MQTTFlaw1: slot propositions, generated vs. gold

Checked on the reachable states of the gold model (depth 12, within the checker bound). precise: the generated proposition never holds where gold is false, and holds somewhere if gold does. recalled: gold never holds where the generated one is false.

## deviceOn: literal (run1, run2, run3, run4, run5)

- gold: `< deviceB | ('status' : true , ..) >`
- generated: `< deviceB | ('on' : true , ..) >`
- renamed: `< deviceB | ( 'status' : true , .. ) >`
- precise True, recalled True

## attackerAuthorized: literal (run1, run2, run3, run4, run5)

- gold: `< cloudB | (userA : ('permission' : true , ..) , ...) >`
- generated: `< cloudB | (userA : ('permission' : true , ..) , ...) >`
- renamed: `< cloudB | ( userA : ( 'permission' : true , .. ) , ... ) >`
- precise True, recalled True

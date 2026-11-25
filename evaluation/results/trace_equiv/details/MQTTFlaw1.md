# MQTTFlaw1: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'cloud:publish' cloudB`
2. `cloudB 'cloud:revoke' cloudB`
3. `userA 'cloud:pubrel' cloudB`
4. `userA 'cloud:publish' cloudB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

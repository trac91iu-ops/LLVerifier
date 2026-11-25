# Sunlogin: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'leaves' deviceB`
3. `userA 'approaches' deviceB`
4. `userC 'approaches' deviceB`
5. `userC 'pressButton' deviceB`
6. `userC 'leaves' deviceB`
7. `userC 'callAPI:bind' cloudA`
8. `userA 'callAPI:bind' cloudA`
9. `userA 'approaches' deviceB`
10. `userC 'approaches' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

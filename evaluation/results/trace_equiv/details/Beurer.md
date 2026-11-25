# Beurer: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'leaves' deviceB`
3. `userA 'approaches' deviceB`
4. `userC 'approaches' deviceB`
5. `userA 'pressButton' deviceB`
6. `userC 'pressButton' deviceB`
7. `userA 'pressButton' deviceB`
8. `userA 'leaves' deviceB`
9. `userC 'pressButton' deviceB`
10. `userC 'leaves' deviceB`
11. `userC 'callAPI:bind' cloudA`
12. `userA 'callAPI:bind' cloudA`
13. `userA 'approaches' deviceB`
14. `userA 'pressButton' deviceB`
15. `userA 'callAPI:bind' cloudA`
16. `userC 'callAPI:bind' cloudA`
17. `userA 'leaves' deviceB`
18. `userC 'approaches' deviceB`
19. `userC 'pressButton' deviceB`
20. `userA 'callAPI:bind' cloudA`
21. `userC 'callAPI:bind' cloudA`
22. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

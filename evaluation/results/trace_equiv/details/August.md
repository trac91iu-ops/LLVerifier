# August: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'leaves' deviceB`
2. `userA 'approaches' deviceB`
3. `userC 'approaches' deviceB`
4. `userC 'pressButton' deviceB`
5. `userA 'pressButton' deviceB`
6. `userC 'callAPI:reset' cloudA`
7. `userA 'leaves' deviceB`
8. `userC 'pressButton' deviceB`
9. `userC 'callAPI:reset' cloudA`
10. `userC 'leaves' deviceB`
11. `userC 'callAPI:bind' cloudA`
12. `userC 'callAPI:reset' cloudA`
13. `userC 'callAPI:bind' cloudA`
14. `userA 'approaches' deviceB`
15. `userA 'pressButton' deviceB`
16. `userC 'callAPI:bind' cloudA`
17. `userC 'callAPI:reset' cloudA`
18. `userA 'leaves' deviceB`
19. `userC 'approaches' deviceB`
20. `userC 'pressButton' deviceB`
21. `userC 'callAPI:bind' cloudA`
22. `userC 'callAPI:reset' cloudA`
23. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

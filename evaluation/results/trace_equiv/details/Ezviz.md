# Ezviz: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'callAPI:reset' cloudA`
2. `userA 'leaves' deviceB`
3. `userA 'approaches' deviceB`
4. `userC 'approaches' deviceB`
5. `userC 'pressButton' deviceB`
6. `userA 'pressButton' deviceB`
7. `userA 'callAPI:reset' cloudA`
8. `userC 'callAPI:reset' cloudA`
9. `userA 'leaves' deviceB`
10. `userC 'pressButton' deviceB`
11. `userC 'callAPI:reset' cloudA`
12. `userC 'leaves' deviceB`
13. `userC 'callAPI:bind' cloudA`
14. `userA 'approaches' deviceB`
15. `userA 'pressButton' deviceB`
16. `userC 'callAPI:bind' cloudA`
17. `userA 'callAPI:reset' cloudA`
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

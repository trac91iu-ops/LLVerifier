# TuyaCAC: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userC 'cloudAPI:toggle' cloudA`
2. `userA 'callAPI:getKey' cloudA`
3. `userC 'cloudAPI:toggle' cloudA`
4. `userC 'callAPI:getKey' cloudA`
5. `userA 'callAPI:invite' cloudA`
6. `userA 'callAPI:getKey' cloudA`
7. `userC 'callAPI:getKey' cloudA`
8. `userA 'callAPI:getKey' cloudA`
9. `userA 'callAPI:invite' cloudA`
10. `userC 'callAPI:invite' cloudA`
11. `userA 'callAPI:getKey' cloudA`
12. `userC 'callAPI:getKey' cloudA`
13. `userA 'callAPI:invite' cloudA`
14. `userA 'callAPI:kick' cloudA`
15. `userC 'callAPI:toggle' deviceB`
16. `userA 'callAPI:toggle' deviceB`
17. `userA 'cloudAPI:toggle' cloudA`
18. `userC 'cloudAPI:toggle' cloudA`
19. `userA 'callAPI:getKey' cloudA`
20. `userC 'callAPI:getKey' cloudA`
21. `userA 'callAPI:invite' cloudA`
22. `userA 'callAPI:toggle' deviceB`
23. `userC 'callAPI:toggle' deviceB`
24. `userA 'cloudAPI:toggle' cloudA`
25. `userC 'cloudAPI:toggle' cloudA`
26. `userA 'callAPI:getKey' cloudA`
27. `userC 'callAPI:getKey' cloudA`
28. `userC 'callAPI:invite' cloudA`
29. `userA 'callAPI:kick' cloudA`
30. `userC 'callAPI:invite' cloudA`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

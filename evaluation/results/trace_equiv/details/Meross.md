# Meross: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'callAPI:bind' cloudA`
3. `userA 'leaves' deviceB`
4. `userA 'callAPI:bind' cloudA`
5. `userA 'approaches' deviceB`
6. `userC 'approaches' deviceB`
7. `userA 'pressButton' deviceB`
8. `userC 'pressButton' deviceB`
9. `userA 'pressButton' deviceB`
10. `userA 'callAPI:bind' cloudA`
11. `userC 'callAPI:bind' cloudA`
12. `userA 'leaves' deviceB`
13. `userC 'pressButton' deviceB`
14. `userA 'callAPI:bind' cloudA`
15. `userC 'callAPI:bind' cloudA`
16. `userC 'leaves' deviceB`
17. `userC 'callAPI:bind' cloudA`
18. `userA 'callAPI:bind' cloudA`
19. `userA 'callAPI:bind' cloudA`
20. `userC 'callAPI:bind' cloudA`
21. `userA 'approaches' deviceB`
22. `userA 'pressButton' deviceB`
23. `userA 'callAPI:bind' cloudA`
24. `userA 'callAPI:bind' cloudA`
25. `userC 'callAPI:bind' cloudA`
26. `userC 'callAPI:bind' cloudA`
27. `userA 'leaves' deviceB`
28. `userC 'approaches' deviceB`
29. `userC 'pressButton' deviceB`
30. `userA 'callAPI:bind' cloudA`
31. `userA 'callAPI:bind' cloudA`
32. `userC 'callAPI:bind' cloudA`
33. `userC 'callAPI:bind' cloudA`
34. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

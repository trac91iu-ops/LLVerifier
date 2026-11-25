# TPLink: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'callAPI:discover' deviceB`
3. `userA 'leaves' deviceB`
4. `userA 'approaches' deviceB`
5. `userC 'approaches' deviceB`
6. `userA 'pressButton' deviceB`
7. `userC 'pressButton' deviceB`
8. `userA 'callAPI:discover' deviceB`
9. `userC 'callAPI:discover' deviceB`
10. `userC 'callAPI:setKey' deviceB`
11. `userA 'pressButton' deviceB`
12. `userC 'pressButton' deviceB`
13. `userA 'callAPI:setKey' deviceB`
14. `userC 'callAPI:setKey' deviceB`
15. `userA 'leaves' deviceB`
16. `userC 'pressButton' deviceB`
17. `userC 'callAPI:setKey' deviceB`
18. `userC 'leaves' deviceB`
19. `userA 'approaches' deviceB`
20. `userA 'callAPI:discover' deviceB`
21. `userA 'pressButton' deviceB`
22. `userA 'callAPI:setKey' deviceB`
23. `userA 'leaves' deviceB`
24. `userA 'approaches' deviceB`
25. `userC 'approaches' deviceB`
26. `userA 'pressButton' deviceB`
27. `userC 'pressButton' deviceB`
28. `userA 'callAPI:discover' deviceB`
29. `userC 'callAPI:discover' deviceB`
30. `userA 'callAPI:setKey' deviceB`
31. `userC 'callAPI:setKey' deviceB`
32. `userA 'leaves' deviceB`
33. `userC 'pressButton' deviceB`
34. `userC 'callAPI:discover' deviceB`
35. `userC 'callAPI:setKey' deviceB`
36. `userC 'leaves' deviceB`
37. `userC 'approaches' deviceB`
38. `userA 'approaches' deviceB`
39. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

# TuyaMatter: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'callAPI:toggle' deviceB`
2. `userC 'callAPI:toggle' deviceB`
3. `userC 'cloudAPI:toggle' cloudA`
4. `userC 'callAPI:openWindow' cloudA`
5. `userA 'callAPI:invite' cloudA`
6. `userA 'callAPI:toggle' deviceB`
7. `userC 'callAPI:toggle' deviceB`
8. `userC 'callAPI:openWindow' cloudA`
9. `userC 'callAPI:bind' deviceB`
10. `userA 'callAPI:toggle' deviceB`
11. `userA 'callAPI:openWindow' cloudA`
12. `userA 'callAPI:bind' deviceB`
13. `userC 'callAPI:bind' deviceB`
14. `userA 'callAPI:toggle' deviceB`
15. `userC 'callAPI:openWindow' cloudA`
16. `userA 'callAPI:invite' cloudA`
17. `userC 'callAPI:invite' cloudA`
18. `userA 'callAPI:bind' deviceB`
19. `userC 'callAPI:bind' deviceB`
20. `userA 'callAPI:toggle' deviceB`
21. `userA 'callAPI:openWindow' cloudA`
22. `userC 'callAPI:openWindow' cloudA`
23. `userA 'callAPI:invite' cloudA`
24. `userA 'callAPI:kick' cloudA`
25. `userA 'callAPI:kick' cloudA`
26. `userC 'callAPI:toggle' deviceB`
27. `userA 'callAPI:bind' deviceB`
28. `userC 'callAPI:bind' deviceB`
29. `cloudA 'callAPI:toggle' deviceB`
30. `userA 'callAPI:toggle' deviceB`
31. `userA 'cloudAPI:toggle' cloudA`
32. `userC 'cloudAPI:toggle' cloudA`
33. `userA 'callAPI:openWindow' cloudA`
34. `userC 'callAPI:openWindow' cloudA`
35. `userA 'callAPI:invite' cloudA`
36. `userA 'callAPI:bind' deviceB`
37. `userC 'callAPI:bind' deviceB`
38. `cloudA 'callAPI:toggle' deviceB`
39. `userA 'callAPI:toggle' deviceB`
40. `userC 'callAPI:toggle' deviceB`
41. `userA 'cloudAPI:toggle' cloudA`
42. `userC 'cloudAPI:toggle' cloudA`
43. `userA 'callAPI:openWindow' cloudA`
44. `userC 'callAPI:openWindow' cloudA`
45. `userC 'callAPI:invite' cloudA`
46. `userA 'callAPI:kick' cloudA`
47. `userA 'callAPI:kick' cloudA`
48. `userC 'callAPI:invite' cloudA`
49. `userA 'callAPI:kick' cloudA`
50. `userC 'callAPI:kick' cloudA`
51. `userC 'callAPI:kick' cloudA`

## run1: gold attack present

## run2: gold attack present

gold events without a generated action (skipped): 3, 31, 32, 41, 42

## run3: gold attack present

gold events without a generated action (skipped): 3, 31, 32, 41, 42

## run4: gold attack present

gold events without a generated action (skipped): 3, 31, 32, 41, 42

## run5: gold attack present

gold events without a generated action (skipped): 3, 31, 32, 41, 42

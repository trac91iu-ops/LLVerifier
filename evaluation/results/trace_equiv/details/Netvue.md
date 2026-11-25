# Netvue: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'pressButton' deviceB`
3. `userA 'pressButton' deviceB`
4. `userA 'callAPI:bind' cloudA`
5. `userA 'callAPI:reset' cloudA`
6. `userC 'callAPI:reset' cloudA`
7. `userA 'leaves' deviceB`
8. `userA 'callAPI:bind' cloudA`
9. `userA 'callAPI:reset' cloudA`
10. `userC 'callAPI:reset' cloudA`
11. `userA 'approaches' deviceB`
12. `userC 'approaches' deviceB`
13. `userC 'pressButton' deviceB`
14. `userA 'callAPI:bind' cloudA`
15. `userC 'callAPI:bind' cloudA`
16. `userA 'callAPI:bind' cloudA`
17. `userA 'callAPI:reset' cloudA`
18. `userC 'callAPI:bind' cloudA`
19. `userC 'callAPI:reset' cloudA`
20. `userA 'callAPI:reset' cloudA`
21. `userA 'leaves' deviceB`
22. `userA 'callAPI:bind' cloudA`
23. `userC 'callAPI:bind' cloudA`
24. `userA 'callAPI:bind' cloudA`
25. `userA 'callAPI:reset' cloudA`
26. `userC 'callAPI:bind' cloudA`
27. `userC 'callAPI:reset' cloudA`
28. `userA 'callAPI:reset' cloudA`
29. `userC 'leaves' deviceB`
30. `userC 'callAPI:bind' cloudA`
31. `userA 'callAPI:bind' cloudA`
32. `userC 'callAPI:bind' cloudA`
33. `userA 'callAPI:reset' cloudA`
34. `userC 'callAPI:reset' cloudA`
35. `userA 'callAPI:bind' cloudA`
36. `userA 'callAPI:reset' cloudA`
37. `userA 'approaches' deviceB`
38. `userA 'callAPI:bind' cloudA`
39. `userC 'callAPI:bind' cloudA`
40. `userA 'callAPI:bind' cloudA`
41. `userA 'callAPI:reset' cloudA`
42. `userC 'callAPI:bind' cloudA`
43. `userC 'callAPI:reset' cloudA`
44. `userA 'callAPI:reset' cloudA`
45. `userA 'leaves' deviceB`
46. `userC 'approaches' deviceB`
47. `userA 'callAPI:bind' cloudA`
48. `userC 'callAPI:bind' cloudA`
49. `userA 'callAPI:bind' cloudA`
50. `userA 'callAPI:reset' cloudA`
51. `userC 'callAPI:bind' cloudA`
52. `userC 'callAPI:reset' cloudA`
53. `userA 'callAPI:reset' cloudA`
54. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

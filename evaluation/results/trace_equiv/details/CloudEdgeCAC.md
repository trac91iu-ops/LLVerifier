# CloudEdgeCAC: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userC 'pressButton' deviceD`
3. `userA 'pressButton' deviceB`
4. `userA 'callAPI:discover' deviceB`
5. `userC 'callAPI:discover' deviceD`
6. `userC 'callAPI:setKey' deviceD`
7. `userA 'pressButton' deviceB`
8. `userC 'pressButton' deviceD`
9. `userA 'pressButton' deviceB`
10. `userA 'callAPI:discover' deviceB`
11. `userC 'callAPI:discover' deviceD`
12. `userA 'pressButton' deviceB`
13. `userC 'pressButton' deviceD`
14. `userA 'callAPI:discover' deviceB`
15. `userC 'callAPI:setKey' deviceD`
16. `userA 'callAPI:setKey' deviceB`
17. `userA 'callAPI:discover' deviceB`
18. `userA 'pressButton' deviceB`
19. `userC 'pressButton' deviceD`
20. `userA 'callAPI:discover' deviceB`
21. `userC 'callAPI:discover' deviceD`
22. `userA 'callAPI:setKey' deviceB`
23. `userC 'callAPI:setKey' deviceD`
24. `userA 'callAPI:setKey' deviceB`
25. `userC 'callAPI:setKey' deviceD`
26. `userA 'leaves' deviceB`
27. `userC 'pressButton' deviceD`
28. `userC 'callAPI:discover' deviceD`
29. `userC 'callAPI:setKey' deviceD`
30. `userC 'callAPI:setKey' deviceD`
31. `userC 'leaves' deviceD`
32. `userA 'approaches' deviceB`
33. `userA 'pressButton' deviceB`
34. `userA 'callAPI:discover' deviceB`
35. `userA 'callAPI:setKey' deviceB`
36. `userA 'callAPI:setKey' deviceB`
37. `userA 'leaves' deviceB`
38. `userC 'approaches' deviceB`
39. `userC 'pressButton' deviceB`
40. `userC 'callAPI:discover' deviceB`
41. `userC 'callAPI:setKey' deviceB`
42. `userC 'callAPI:setKey' deviceB`
43. `userC 'leaves' deviceB`
44. `userA 'approaches' deviceD`
45. `userA 'pressButton' deviceD`
46. `userA 'callAPI:discover' deviceD`
47. `userA 'callAPI:setKey' deviceD`
48. `userA 'callAPI:setKey' deviceD`
49. `userA 'leaves' deviceD`
50. `userC 'approaches' deviceD`
51. `userA 'approaches' deviceB`
52. `userC 'leaves' deviceD`
53. `userC 'approaches' deviceB`
54. `userA 'pressButton' deviceB`
55. `userC 'pressButton' deviceB`
56. `userA 'callAPI:discover' deviceB`
57. `userC 'callAPI:discover' deviceB`
58. `userA 'callAPI:setKey' deviceB`
59. `userC 'callAPI:setKey' deviceB`
60. `userA 'callAPI:setKey' deviceB`
61. `userC 'callAPI:setKey' deviceB`
62. `userA 'leaves' deviceB`
63. `userA 'approaches' deviceB`
64. `userC 'leaves' deviceB`
65. `userC 'approaches' deviceD`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

# CloudEdgeRTE: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'presses' deviceB`
2. `userC 'presses' deviceD`
3. `userA 'presses' deviceB`
4. `userA 'callAPI:discover' deviceB`
5. `userC 'callAPI:discover' deviceD`
6. `userA 'callAPI:setKey' deviceB`
7. `userA 'presses' deviceB`
8. `userC 'presses' deviceD`
9. `userA 'callAPI:discover' deviceB`
10. `userA 'presses' deviceB`
11. `userC 'presses' deviceD`
12. `userC 'callAPI:discover' deviceD`
13. `userA 'callAPI:setKey' deviceB`
14. `userC 'callAPI:setKey' deviceD`
15. `userC 'callAPI:discover' deviceD`
16. `userA 'presses' deviceB`
17. `userC 'presses' deviceD`
18. `userA 'presses' deviceB`
19. `userA 'callAPI:discover' deviceB`
20. `userC 'callAPI:discover' deviceD`
21. `userA 'callAPI:setKey' deviceB`
22. `userC 'callAPI:setKey' deviceD`
23. `userA 'callAPI:setKey' deviceB`
24. `userC 'callAPI:setKey' deviceD`
25. `userA 'leaves' deviceB`
26. `userC 'presses' deviceD`
27. `userC 'callAPI:discover' deviceD`
28. `userC 'callAPI:setKey' deviceD`
29. `userC 'callAPI:setKey' deviceD`
30. `userC 'leaves' deviceD`
31. `userA 'approaches' deviceB`
32. `userA 'presses' deviceB`
33. `userA 'callAPI:discover' deviceB`
34. `userA 'callAPI:setKey' deviceB`
35. `userA 'callAPI:setKey' deviceB`
36. `userA 'leaves' deviceB`
37. `userA 'approaches' deviceD`
38. `userA 'presses' deviceD`
39. `userA 'callAPI:discover' deviceD`
40. `userA 'callAPI:setKey' deviceD`
41. `userA 'callAPI:setKey' deviceD`
42. `userA 'leaves' deviceD`
43. `userC 'approaches' deviceB`
44. `userC 'presses' deviceB`
45. `userC 'callAPI:discover' deviceB`
46. `userC 'callAPI:setKey' deviceB`
47. `userC 'callAPI:setKey' deviceB`
48. `userC 'leaves' deviceB`
49. `userC 'approaches' deviceD`
50. `userA 'approaches' deviceB`
51. `userC 'leaves' deviceD`
52. `userC 'approaches' deviceB`
53. `userA 'presses' deviceB`
54. `userC 'presses' deviceB`
55. `userA 'callAPI:discover' deviceB`
56. `userC 'callAPI:discover' deviceB`
57. `userA 'callAPI:setKey' deviceB`
58. `userC 'callAPI:setKey' deviceB`
59. `userA 'callAPI:setKey' deviceB`
60. `userC 'callAPI:setKey' deviceB`
61. `userA 'leaves' deviceB`
62. `userA 'approaches' deviceB`
63. `userC 'leaves' deviceB`
64. `userC 'approaches' deviceD`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

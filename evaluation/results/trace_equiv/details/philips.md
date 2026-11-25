# philips: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'pressButton' deviceB`
3. `userA 'pressButton' deviceB`
4. `userA 'pressButton' deviceB`
5. `userA 'callAPI:getKey' cloudA`
6. `userA 'callAPI:bind' cloudA`
7. `userA 'callAPI:getKey' cloudA`
8. `userA 'callAPI:join' cloudA`
9. `userA 'leaves' deviceB`
10. `userA 'callAPI:bind' cloudA`
11. `userA 'callAPI:join' cloudA`
12. `userA 'approaches' deviceB`
13. `userC 'approaches' deviceB`
14. `userA 'callAPI:getKey' cloudA`
15. `userC 'callAPI:getKey' cloudA`
16. `userA 'callAPI:getKey' cloudA`
17. `userA 'callAPI:bind' cloudA`
18. `userC 'callAPI:bind' cloudA`
19. `userA 'callAPI:join' cloudA`
20. `userA 'leaves' deviceB`
21. `userC 'callAPI:getKey' cloudA`
22. `userA 'callAPI:bind' cloudA`
23. `userC 'callAPI:bind' cloudA`
24. `userA 'callAPI:join' cloudA`
25. `userC 'leaves' deviceB`
26. `userC 'callAPI:join' cloudA`
27. `userA 'callAPI:bind' cloudA`
28. `userC 'callAPI:bind' cloudA`
29. `userA 'callAPI:join' cloudA`
30. `userA 'approaches' deviceB`
31. `userA 'callAPI:getKey' cloudA`
32. `userA 'callAPI:bind' cloudA`
33. `userC 'callAPI:bind' cloudA`
34. `userA 'callAPI:join' cloudA`
35. `userC 'callAPI:join' cloudA`
36. `userA 'leaves' deviceB`
37. `userC 'approaches' deviceB`
38. `userC 'callAPI:getKey' cloudA`
39. `userA 'callAPI:bind' cloudA`
40. `userC 'callAPI:bind' cloudA`
41. `userA 'callAPI:join' cloudA`
42. `userC 'callAPI:join' cloudA`
43. `userC 'leaves' deviceB`
44. `userA 'callAPI:bind' cloudA`
45. `userC 'callAPI:bind' cloudA`
46. `userA 'callAPI:join' cloudA`
47. `userC 'callAPI:join' cloudA`
48. `userA 'approaches' deviceB`
49. `userA 'callAPI:getKey' cloudA`
50. `userA 'callAPI:bind' cloudA`
51. `userC 'callAPI:bind' cloudA`
52. `userA 'callAPI:join' cloudA`
53. `userC 'callAPI:join' cloudA`
54. `userA 'leaves' deviceB`
55. `userC 'approaches' deviceB`
56. `userC 'callAPI:getKey' cloudA`
57. `userA 'callAPI:bind' cloudA`
58. `userC 'callAPI:bind' cloudA`
59. `userA 'callAPI:join' cloudA`
60. `userC 'callAPI:join' cloudA`
61. `userC 'leaves' deviceB`
62. `userA 'callAPI:bind' cloudA`
63. `userC 'callAPI:bind' cloudA`
64. `userA 'callAPI:join' cloudA`
65. `userC 'callAPI:join' cloudA`
66. `userA 'approaches' deviceB`
67. `userA 'callAPI:getKey' cloudA`
68. `userA 'callAPI:bind' cloudA`
69. `userC 'callAPI:bind' cloudA`
70. `userA 'callAPI:join' cloudA`
71. `userC 'callAPI:join' cloudA`
72. `userA 'leaves' deviceB`
73. `userC 'approaches' deviceB`
74. `userC 'callAPI:getKey' cloudA`
75. `userA 'callAPI:bind' cloudA`
76. `userC 'callAPI:bind' cloudA`
77. `userA 'callAPI:join' cloudA`
78. `userC 'callAPI:join' cloudA`
79. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

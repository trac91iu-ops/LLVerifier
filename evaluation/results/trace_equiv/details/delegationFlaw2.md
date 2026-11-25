# delegationFlaw2: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'callAPI:getKey' cloudB`
2. `userC 'callAPI:getKey' cloudB`
3. `userA 'callAPI:getKey' cloudSmartThing`
4. `userA 'callAPI:getKey' cloudB`
5. `userC 'callAPI:getKey' cloudB`
6. `userC 'callAPI:getKey' cloudSmartThing`
7. `userA 'callAPI:delegate' cloudB`
8. `userC 'callAPI:delegate' cloudB`
9. `userA 'callAPI:delegate' cloudB`
10. `userC 'callAPI:delegate' cloudB`
11. `userA 'callAPI:delegate' cloudSmartThing`
12. `userC 'callAPI:delegate' cloudSmartThing`
13. `userA 'callAPI:delegate' cloudSmartThing`
14. `userA 'callAPI:getKey' cloudB`
15. `userC 'callAPI:getKey' cloudB`
16. `userA 'callAPI:getKey' cloudSmartThing`
17. `userC 'callAPI:getKey' cloudSmartThing`
18. `userA 'callAPI:getKey' cloudB`
19. `userC 'callAPI:getKey' cloudB`
20. `userA 'callAPI:getKey' cloudSmartThing`
21. `userA 'callAPI:delegate' cloudB`
22. `userC 'callAPI:delegate' cloudB`
23. `userA 'callAPI:delegate' cloudB`
24. `userC 'callAPI:delegate' cloudB`
25. `userA 'callAPI:delegate' cloudSmartThing`
26. `userC 'callAPI:delegate' cloudSmartThing`
27. `userA 'callAPI:delegate' cloudSmartThing`
28. `userC 'callAPI:delegate' cloudSmartThing`
29. `userA 'callAPI:revoke' cloudB`
30. `userC 'callAPI:revoke' cloudB`
31. `userA 'callAPI:revoke' cloudB`
32. `userC 'callAPI:revoke' cloudB`
33. `userA 'callAPI:revoke' cloudSmartThing`
34. `userC 'callAPI:revoke' cloudSmartThing`
35. `userA 'callAPI:revoke' cloudSmartThing`
36. `userC 'callAPI:cloudAPI:toggle' cloudSmartThing`
37. `userA 'callAPI:getKey' cloudB`
38. `userC 'callAPI:getKey' cloudB`
39. `userA 'callAPI:getKey' cloudSmartThing`
40. `userC 'callAPI:getKey' cloudSmartThing`
41. `userA 'callAPI:delegate' cloudB`
42. `userC 'callAPI:delegate' cloudB`
43. `userA 'callAPI:delegate' cloudB`
44. `userC 'callAPI:delegate' cloudB`
45. `userA 'callAPI:delegate' cloudSmartThing`
46. `userC 'callAPI:delegate' cloudSmartThing`
47. `userA 'callAPI:delegate' cloudSmartThing`
48. `userA 'callAPI:getKey' cloudB`
49. `userC 'callAPI:getKey' cloudB`
50. `userA 'callAPI:getKey' cloudSmartThing`
51. `userC 'callAPI:getKey' cloudSmartThing`
52. `userA 'callAPI:delegate' cloudB`
53. `userC 'callAPI:delegate' cloudB`
54. `userA 'callAPI:delegate' cloudB`
55. `userC 'callAPI:delegate' cloudB`
56. `userA 'callAPI:delegate' cloudSmartThing`
57. `userC 'callAPI:delegate' cloudSmartThing`
58. `userC 'callAPI:delegate' cloudSmartThing`
59. `userA 'callAPI:revoke' cloudB`
60. `userC 'callAPI:revoke' cloudB`
61. `userA 'callAPI:revoke' cloudB`
62. `userC 'callAPI:revoke' cloudB`
63. `userA 'callAPI:revoke' cloudSmartThing`
64. `userC 'callAPI:revoke' cloudSmartThing`
65. `userA 'callAPI:revoke' cloudSmartThing`
66. `userC 'callAPI:delegate' cloudSmartThing`
67. `userA 'callAPI:revoke' cloudB`
68. `userC 'callAPI:revoke' cloudB`
69. `userA 'callAPI:revoke' cloudB`
70. `userC 'callAPI:revoke' cloudB`
71. `userA 'callAPI:revoke' cloudSmartThing`
72. `userC 'callAPI:revoke' cloudSmartThing`
73. `userC 'callAPI:revoke' cloudSmartThing`
74. `userA 'callAPI:cloudAPI:toggle' cloudSmartThing`
75. `userC 'callAPI:cloudAPI:toggle' cloudSmartThing`
76. `userA 'callAPI:cloudAPI:toggle' cloudSmartThing`
77. `userA 'callAPI:toggle' deviceLock`
78. `userC 'callAPI:toggle' deviceLock`
79. `userA 'callAPI:toggle' deviceSwitch`
80. `userC 'callAPI:toggle' deviceSwitch`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

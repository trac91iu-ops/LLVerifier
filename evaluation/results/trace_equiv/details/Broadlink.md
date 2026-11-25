# Broadlink: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'pressButton' deviceB`
3. `userA 'pressButton' deviceB`
4. `userA 'pressButton' deviceB`
5. `userA 'callAPI:getKey' deviceB`
6. `userA 'cloudAPI:getKey' cloudA`
7. `userC 'callAPI:invite' cloudA`
8. `userA 'callAPI:getKey' deviceB`
9. `userA 'cloudAPI:getKey' cloudA`
10. `userC 'callAPI:kick' cloudA`
11. `userA 'leaves' deviceB`
12. `userA 'cloudAPI:getKey' cloudA`
13. `userC 'callAPI:invite' cloudA`
14. `userA 'cloudAPI:getKey' cloudA`
15. `userC 'callAPI:kick' cloudA`
16. `userA 'approaches' deviceB`
17. `userC 'approaches' deviceB`
18. `userA 'callAPI:getKey' deviceB`
19. `userC 'callAPI:getKey' deviceB`
20. `userA 'callAPI:getKey' deviceB`
21. `userA 'callAPI:lock' deviceB`
22. `userA 'callAPI:getKey' deviceB`
23. `userC 'callAPI:getKey' deviceB`
24. `userC 'callAPI:lock' deviceB`
25. `userA 'cloudAPI:getKey' cloudA`
26. `userC 'cloudAPI:getKey' cloudA`
27. `userC 'callAPI:invite' cloudA`
28. `userA 'callAPI:getKey' deviceB`
29. `userC 'callAPI:getKey' deviceB`
30. `userA 'callAPI:lock' deviceB`
31. `userC 'callAPI:lock' deviceB`
32. `userA 'cloudAPI:getKey' cloudA`
33. `userC 'cloudAPI:getKey' cloudA`
34. `userC 'callAPI:kick' cloudA`
35. `userA 'leaves' deviceB`
36. `userC 'callAPI:getKey' deviceB`
37. `userC 'callAPI:lock' deviceB`
38. `userA 'cloudAPI:getKey' cloudA`
39. `userC 'cloudAPI:getKey' cloudA`
40. `userC 'callAPI:invite' cloudA`
41. `userC 'callAPI:getKey' deviceB`
42. `userC 'callAPI:lock' deviceB`
43. `userA 'cloudAPI:getKey' cloudA`
44. `userC 'cloudAPI:getKey' cloudA`
45. `userC 'callAPI:kick' cloudA`
46. `userC 'leaves' deviceB`
47. `userC 'callAPI:bind' cloudA`
48. `userA 'callAPI:bind' cloudA`
49. `userC 'callAPI:bind' cloudA`
50. `userA 'cloudAPI:getKey' cloudA`
51. `userC 'cloudAPI:getKey' cloudA`
52. `userC 'callAPI:invite' cloudA`
53. `userA 'callAPI:bind' cloudA`
54. `userC 'callAPI:bind' cloudA`
55. `userA 'cloudAPI:getKey' cloudA`
56. `userC 'cloudAPI:getKey' cloudA`
57. `userC 'callAPI:kick' cloudA`
58. `userA 'approaches' deviceB`
59. `userA 'callAPI:getKey' deviceB`
60. `userA 'callAPI:lock' deviceB`
61. `userA 'callAPI:bind' cloudA`
62. `userC 'callAPI:bind' cloudA`
63. `userA 'cloudAPI:getKey' cloudA`
64. `userC 'cloudAPI:getKey' cloudA`
65. `userC 'callAPI:invite' cloudA`
66. `userA 'callAPI:getKey' deviceB`
67. `userA 'callAPI:lock' deviceB`
68. `userA 'callAPI:bind' cloudA`
69. `userC 'callAPI:bind' cloudA`
70. `userA 'cloudAPI:getKey' cloudA`
71. `userC 'cloudAPI:getKey' cloudA`
72. `userC 'callAPI:kick' cloudA`
73. `userA 'leaves' deviceB`
74. `userC 'approaches' deviceB`
75. `userC 'callAPI:getKey' deviceB`
76. `userC 'callAPI:lock' deviceB`
77. `userA 'callAPI:bind' cloudA`
78. `userC 'callAPI:bind' cloudA`
79. `userA 'cloudAPI:getKey' cloudA`
80. `userC 'cloudAPI:getKey' cloudA`
81. `userC 'callAPI:invite' cloudA`
82. `userC 'callAPI:getKey' deviceB`
83. `userC 'callAPI:lock' deviceB`
84. `userA 'callAPI:bind' cloudA`
85. `userC 'callAPI:bind' cloudA`
86. `userA 'cloudAPI:getKey' cloudA`
87. `userC 'cloudAPI:getKey' cloudA`
88. `userC 'callAPI:kick' cloudA`
89. `userC 'leaves' deviceB`

## run1: model did not load

## run2: model did not load

## run3: gold attack present

## run4: model did not load

## run5: gold attack present

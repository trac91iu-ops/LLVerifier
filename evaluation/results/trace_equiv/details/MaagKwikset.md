# MaagKwikset: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'callAPI:getKey' deviceB`
2. `userA 'callAPI:signKey' cloudA`
3. `userA 'callAPI:getKey' deviceB`
4. `userA 'callAPI:bind' deviceB`
5. `userA 'callAPI:share' cloudA`
6. `userA 'callAPI:getKey' deviceB`
7. `userA 'callAPI:bind' deviceB`
8. `userA 'callAPI:signKey' cloudA`
9. `userC 'callAPI:share' cloudA`
10. `userA 'callAPI:revoke' cloudA`
11. `userC 'callAPI:share' cloudA`
12. `userC 'callAPI:revoke' cloudA`
13. `userA 'leaves' deviceB`
14. `userA 'callAPI:signKey' cloudA`
15. `userA 'callAPI:share' cloudA`
16. `userA 'callAPI:signKey' cloudA`
17. `userC 'callAPI:share' cloudA`
18. `userA 'callAPI:revoke' cloudA`
19. `userC 'callAPI:share' cloudA`
20. `userC 'callAPI:revoke' cloudA`
21. `userA 'approaches' deviceB`
22. `userC 'approaches' deviceB`
23. `userA 'callAPI:getKey' deviceB`
24. `userC 'callAPI:getKey' deviceB`
25. `userA 'callAPI:getKey' deviceB`
26. `userA 'callAPI:bind' deviceB`
27. `userA 'callAPI:signKey' cloudA`
28. `userC 'callAPI:signKey' cloudA`
29. `userA 'callAPI:share' cloudA`
30. `userA 'callAPI:getKey' deviceB`
31. `userC 'callAPI:getKey' deviceB`
32. `userA 'callAPI:bind' deviceB`
33. `userA 'callAPI:signKey' cloudA`
34. `userC 'callAPI:signKey' cloudA`
35. `userA 'callAPI:getKey' deviceB`
36. `userC 'callAPI:getKey' deviceB`
37. `userA 'callAPI:bind' deviceB`
38. `userA 'callAPI:signKey' cloudA`
39. `userA 'callAPI:share' cloudA`
40. `userC 'callAPI:share' cloudA`
41. `userA 'callAPI:revoke' cloudA`
42. `userC 'callAPI:bind' deviceB`
43. `userA 'callAPI:getKey' deviceB`
44. `userC 'callAPI:getKey' deviceB`
45. `userA 'callAPI:bind' deviceB`
46. `userA 'callAPI:signKey' cloudA`
47. `userC 'callAPI:signKey' cloudA`
48. `userA 'callAPI:share' cloudA`
49. `userA 'callAPI:getKey' deviceB`
50. `userC 'callAPI:getKey' deviceB`
51. `userA 'callAPI:bind' deviceB`
52. `userC 'callAPI:bind' deviceB`
53. `userA 'callAPI:signKey' cloudA`
54. `userC 'callAPI:signKey' cloudA`
55. `userC 'callAPI:share' cloudA`
56. `userA 'callAPI:revoke' cloudA`
57. `userC 'callAPI:share' cloudA`
58. `userC 'callAPI:revoke' cloudA`
59. `userA 'leaves' deviceB`
60. `userC 'callAPI:getKey' deviceB`
61. `userC 'callAPI:bind' deviceB`
62. `userA 'callAPI:signKey' cloudA`
63. `userC 'callAPI:signKey' cloudA`
64. `userA 'callAPI:share' cloudA`
65. `userC 'callAPI:getKey' deviceB`
66. `userC 'callAPI:bind' deviceB`
67. `userA 'callAPI:signKey' cloudA`
68. `userC 'callAPI:signKey' cloudA`
69. `userC 'callAPI:share' cloudA`
70. `userA 'callAPI:revoke' cloudA`
71. `userC 'callAPI:share' cloudA`
72. `userC 'callAPI:revoke' cloudA`
73. `userC 'leaves' deviceB`
74. `userA 'callAPI:signKey' cloudA`
75. `userC 'callAPI:signKey' cloudA`
76. `userA 'callAPI:share' cloudA`
77. `userA 'callAPI:signKey' cloudA`
78. `userC 'callAPI:signKey' cloudA`
79. `userC 'callAPI:share' cloudA`
80. `userA 'callAPI:revoke' cloudA`
81. `userC 'callAPI:share' cloudA`
82. `userC 'callAPI:revoke' cloudA`
83. `userA 'approaches' deviceB`
84. `userA 'callAPI:getKey' deviceB`
85. `userA 'callAPI:bind' deviceB`
86. `userA 'callAPI:signKey' cloudA`
87. `userC 'callAPI:signKey' cloudA`
88. `userA 'callAPI:share' cloudA`
89. `userA 'callAPI:getKey' deviceB`
90. `userA 'callAPI:bind' deviceB`
91. `userA 'callAPI:signKey' cloudA`
92. `userC 'callAPI:signKey' cloudA`
93. `userC 'callAPI:share' cloudA`
94. `userA 'callAPI:revoke' cloudA`
95. `userC 'callAPI:share' cloudA`
96. `userC 'callAPI:revoke' cloudA`
97. `userA 'leaves' deviceB`
98. `userC 'approaches' deviceB`
99. `userA 'approaches' deviceB`
100. `userC 'leaves' deviceB`
101. `userC 'approaches' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

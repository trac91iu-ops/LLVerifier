# Midea: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'callAPI:bind' cloudA`
3. `userA 'pressButton' deviceB`
4. `userA 'callAPI:reset' cloudA`
5. `userA 'callAPI:bind' cloudA`
6. `userC 'callAPI:reset' cloudA`
7. `userA 'leaves' deviceB`
8. `userA 'callAPI:bind' cloudA`
9. `userA 'callAPI:reset' cloudA`
10. `userC 'callAPI:reset' cloudA`
11. `userA 'approaches' deviceB`
12. `userC 'approaches' deviceB`
13. `userA 'pressButton' deviceB`
14. `userC 'pressButton' deviceB`
15. `userA 'callAPI:bind' cloudA`
16. `userA 'pressButton' deviceB`
17. `userC 'pressButton' deviceB`
18. `userA 'callAPI:reset' cloudA`
19. `userC 'pressButton' deviceB`
20. `userA 'pressButton' deviceB`
21. `userA 'callAPI:bind' cloudA`
22. `userA 'pressButton' deviceB`
23. `userC 'pressButton' deviceB`
24. `userC 'callAPI:bind' cloudA`
25. `userA 'callAPI:reset' cloudA`
26. `userA 'callAPI:bind' cloudA`
27. `userC 'callAPI:bind' cloudA`
28. `userC 'callAPI:reset' cloudA`
29. `userA 'leaves' deviceB`
30. `userC 'pressButton' deviceB`
31. `userA 'callAPI:bind' cloudA`
32. `userC 'pressButton' deviceB`
33. `userC 'callAPI:bind' cloudA`
34. `userA 'callAPI:reset' cloudA`
35. `userA 'callAPI:bind' cloudA`
36. `userC 'callAPI:bind' cloudA`
37. `userC 'callAPI:reset' cloudA`
38. `userC 'leaves' deviceB`
39. `userA 'callAPI:bind' cloudA`
40. `userC 'callAPI:bind' cloudA`
41. `userA 'callAPI:reset' cloudA`
42. `userC 'callAPI:reset' cloudA`
43. `userA 'approaches' deviceB`
44. `userA 'pressButton' deviceB`
45. `userC 'callAPI:bind' cloudA`
46. `userA 'pressButton' deviceB`
47. `userA 'callAPI:bind' cloudA`
48. `userA 'callAPI:reset' cloudA`
49. `userC 'callAPI:reset' cloudA`
50. `userA 'pressButton' deviceB`
51. `userA 'callAPI:bind' cloudA`
52. `userA 'pressButton' deviceB`
53. `userC 'callAPI:bind' cloudA`
54. `userA 'callAPI:reset' cloudA`
55. `userA 'callAPI:bind' cloudA`
56. `userC 'callAPI:bind' cloudA`
57. `userA 'leaves' deviceB`
58. `userA 'callAPI:bind' cloudA`
59. `userC 'callAPI:bind' cloudA`
60. `userA 'callAPI:reset' cloudA`
61. `userC 'callAPI:reset' cloudA`
62. `userA 'approaches' deviceB`
63. `userC 'approaches' deviceB`
64. `userA 'pressButton' deviceB`
65. `userC 'pressButton' deviceB`
66. `userA 'callAPI:bind' cloudA`
67. `userA 'pressButton' deviceB`
68. `userC 'pressButton' deviceB`
69. `userC 'callAPI:bind' cloudA`
70. `userA 'callAPI:reset' cloudA`
71. `userA 'callAPI:bind' cloudA`
72. `userC 'callAPI:bind' cloudA`
73. `userC 'callAPI:reset' cloudA`
74. `userA 'leaves' deviceB`
75. `userC 'pressButton' deviceB`
76. `userA 'callAPI:bind' cloudA`
77. `userC 'pressButton' deviceB`
78. `userC 'callAPI:bind' cloudA`
79. `userA 'callAPI:reset' cloudA`
80. `userA 'callAPI:bind' cloudA`
81. `userC 'callAPI:bind' cloudA`
82. `userC 'callAPI:reset' cloudA`
83. `userC 'leaves' deviceB`
84. `userC 'approaches' deviceB`
85. `userA 'approaches' deviceB`
86. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

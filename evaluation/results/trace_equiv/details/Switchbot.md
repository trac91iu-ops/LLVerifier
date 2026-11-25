# Switchbot: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'pressButton' deviceB`
2. `userA 'callAPI:bind' cloudA`
3. `userA 'pressButton' deviceB`
4. `userA 'callAPI:invite' cloudA`
5. `userA 'pressButton' deviceB`
6. `userA 'callAPI:bind' cloudA`
7. `userA 'callAPI:kick' cloudA`
8. `userC 'callAPI:invite' cloudA`
9. `userA 'pressButton' deviceB`
10. `userA 'callAPI:bind' cloudA`
11. `userA 'callAPI:invite' cloudA`
12. `userA 'pressButton' deviceB`
13. `userA 'callAPI:bind' cloudA`
14. `userA 'callAPI:kick' cloudA`
15. `userC 'callAPI:kick' cloudA`
16. `userA 'leaves' deviceB`
17. `userA 'callAPI:bind' cloudA`
18. `userA 'callAPI:invite' cloudA`
19. `userA 'callAPI:bind' cloudA`
20. `userA 'callAPI:kick' cloudA`
21. `userC 'callAPI:invite' cloudA`
22. `userA 'callAPI:bind' cloudA`
23. `userA 'callAPI:invite' cloudA`
24. `userA 'callAPI:bind' cloudA`
25. `userA 'callAPI:kick' cloudA`
26. `userC 'callAPI:kick' cloudA`
27. `userA 'approaches' deviceB`
28. `userC 'approaches' deviceB`
29. `userA 'pressButton' deviceB`
30. `userC 'pressButton' deviceB`
31. `userA 'pressButton' deviceB`
32. `userA 'callAPI:bind' cloudA`
33. `userA 'callAPI:invite' cloudA`
34. `userA 'pressButton' deviceB`
35. `userC 'pressButton' deviceB`
36. `userA 'callAPI:bind' cloudA`
37. `userA 'callAPI:kick' cloudA`
38. `userC 'callAPI:invite' cloudA`
39. `userA 'pressButton' deviceB`
40. `userC 'pressButton' deviceB`
41. `userA 'callAPI:bind' cloudA`
42. `userA 'callAPI:invite' cloudA`
43. `userA 'pressButton' deviceB`
44. `userC 'pressButton' deviceB`
45. `userA 'callAPI:bind' cloudA`
46. `userA 'callAPI:kick' cloudA`
47. `userC 'callAPI:kick' cloudA`
48. `userA 'leaves' deviceB`
49. `userC 'pressButton' deviceB`
50. `userA 'callAPI:bind' cloudA`
51. `userA 'callAPI:invite' cloudA`
52. `userC 'pressButton' deviceB`
53. `userA 'callAPI:bind' cloudA`
54. `userA 'callAPI:kick' cloudA`
55. `userC 'callAPI:invite' cloudA`
56. `userC 'pressButton' deviceB`
57. `userA 'callAPI:bind' cloudA`
58. `userA 'callAPI:invite' cloudA`
59. `userC 'pressButton' deviceB`
60. `userA 'callAPI:bind' cloudA`
61. `userA 'callAPI:kick' cloudA`
62. `userC 'callAPI:kick' cloudA`
63. `userC 'leaves' deviceB`
64. `userC 'callAPI:bind' cloudA`
65. `userA 'callAPI:bind' cloudA`
66. `userA 'callAPI:invite' cloudA`
67. `userA 'callAPI:bind' cloudA`
68. `userC 'callAPI:bind' cloudA`
69. `userA 'callAPI:kick' cloudA`
70. `userC 'callAPI:invite' cloudA`
71. `userA 'callAPI:bind' cloudA`
72. `userC 'callAPI:bind' cloudA`
73. `userA 'callAPI:invite' cloudA`
74. `userA 'callAPI:bind' cloudA`
75. `userC 'callAPI:bind' cloudA`
76. `userA 'callAPI:kick' cloudA`
77. `userC 'callAPI:kick' cloudA`
78. `userA 'approaches' deviceB`
79. `userA 'pressButton' deviceB`
80. `userA 'callAPI:bind' cloudA`
81. `userC 'callAPI:bind' cloudA`
82. `userA 'callAPI:invite' cloudA`
83. `userA 'pressButton' deviceB`
84. `userA 'callAPI:bind' cloudA`
85. `userC 'callAPI:bind' cloudA`
86. `userA 'callAPI:kick' cloudA`
87. `userC 'callAPI:invite' cloudA`
88. `userA 'pressButton' deviceB`
89. `userA 'callAPI:bind' cloudA`
90. `userC 'callAPI:bind' cloudA`
91. `userA 'callAPI:invite' cloudA`
92. `userA 'pressButton' deviceB`
93. `userA 'callAPI:bind' cloudA`
94. `userC 'callAPI:bind' cloudA`
95. `userA 'callAPI:kick' cloudA`
96. `userC 'callAPI:kick' cloudA`
97. `userA 'leaves' deviceB`
98. `userC 'approaches' deviceB`
99. `userC 'pressButton' deviceB`
100. `userA 'callAPI:bind' cloudA`
101. `userC 'callAPI:bind' cloudA`
102. `userA 'callAPI:invite' cloudA`
103. `userC 'pressButton' deviceB`
104. `userA 'callAPI:bind' cloudA`
105. `userC 'callAPI:bind' cloudA`
106. `userA 'callAPI:kick' cloudA`
107. `userC 'callAPI:invite' cloudA`
108. `userC 'pressButton' deviceB`
109. `userA 'callAPI:bind' cloudA`
110. `userC 'callAPI:bind' cloudA`
111. `userA 'callAPI:invite' cloudA`
112. `userC 'pressButton' deviceB`
113. `userA 'callAPI:bind' cloudA`
114. `userC 'callAPI:bind' cloudA`
115. `userA 'callAPI:kick' cloudA`
116. `userC 'callAPI:kick' cloudA`
117. `userC 'leaves' deviceB`

## run1: gold attack present

## run2: gold attack present

## run3: gold attack present

## run4: gold attack present

## run5: gold attack present

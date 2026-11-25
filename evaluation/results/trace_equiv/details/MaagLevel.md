# MaagLevel: gold counterexample replayed in the generated models

Gold trace (modelCheck on the gold model: prefix, then one round of the cycle):

1. `userA 'callAPI:share' cloudA`
2. `userC 'callAPI:share' cloudA`
3. `userA 'callAPI:revoke' cloudA`
4. `userC 'callAPI:revoke' cloudA`
5. `userA 'approaches' deviceB`
6. `userA 'callAPI:share' cloudA`
7. `userC 'callAPI:share' cloudA`
8. `userA 'callAPI:revoke' cloudA`
9. `userC 'callAPI:share' cloudA`
10. `userC 'callAPI:revoke' cloudA`
11. `userA 'leaves' deviceB`
12. `userC 'approaches' deviceB`
13. `userA 'callAPI:share' cloudA`
14. `userC 'callAPI:share' cloudA`
15. `userA 'callAPI:revoke' cloudA`
16. `userC 'callAPI:proxy' deviceB`
17. `userA 'callAPI:share' cloudA`
18. `userC 'callAPI:share' cloudA`
19. `userA 'callAPI:revoke' cloudA`
20. `userC 'callAPI:share' cloudA`
21. `userC 'callAPI:revoke' cloudA`
22. `userC 'leaves' deviceB`
23. `userA 'callAPI:share' cloudA`
24. `userC 'callAPI:share' cloudA`
25. `userA 'callAPI:revoke' cloudA`
26. `userC 'callAPI:revoke' cloudA`
27. `userA 'approaches' deviceB`
28. `userA 'callAPI:share' cloudA`
29. `userC 'callAPI:share' cloudA`
30. `userA 'callAPI:revoke' cloudA`
31. `userC 'callAPI:share' cloudA`
32. `userC 'callAPI:revoke' cloudA`
33. `userA 'leaves' deviceB`
34. `userA 'callAPI:share' cloudA`
35. `userC 'callAPI:share' cloudA`
36. `userA 'callAPI:revoke' cloudA`
37. `userC 'callAPI:revoke' cloudA`
38. `userA 'approaches' deviceB`
39. `userC 'approaches' deviceB`
40. `userA 'callAPI:share' cloudA`
41. `userC 'callAPI:share' cloudA`
42. `userA 'callAPI:revoke' cloudA`
43. `userC 'callAPI:share' cloudA`
44. `userC 'callAPI:revoke' cloudA`
45. `userC 'callAPI:proxy' deviceB`
46. `userA 'callAPI:share' cloudA`
47. `userC 'callAPI:share' cloudA`
48. `userA 'callAPI:revoke' cloudA`
49. `userC 'callAPI:share' cloudA`
50. `userC 'callAPI:revoke' cloudA`
51. `userA 'leaves' deviceB`
52. `userA 'callAPI:share' cloudA`
53. `userC 'callAPI:share' cloudA`
54. `userA 'callAPI:revoke' cloudA`
55. `userC 'callAPI:share' cloudA`
56. `userC 'callAPI:revoke' cloudA`
57. `userC 'leaves' deviceB`
58. `userC 'approaches' deviceB`
59. `userA 'approaches' deviceB`
60. `userA 'leaves' deviceB`

## run1: gold attack not present

## run2: gold attack not present

## run3: gold attack not present

## run4: gold attack not present

## run5: gold attack not present

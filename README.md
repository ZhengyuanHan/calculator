Member1:

Name: Zhengyuan Han

Stevens-mail: zhan24@stevens.edu

CWID: 20011343

Member2:

Name: Nithin Reddy Gutha

Stevens-mail: ngutha@stevens.edu

CWID: 

GitHub repo: https://github.com/ZhengyuanHan/calculator.git

We spent about 20 hours on the project.

We used the examples on canvas and other similar expressions to test our code.

Bugs or issues we could not resolve:

1. We did not know what "parse errors" exactly looks like, perhaps we need more examples.
2. There some unclear fails on gradescope.
3. Maybe some extrem situations we did not consider.

difficult issue or bug we resolved:

We think the most diffcult issue is parsing expressions. Including extentions, there are many kinds of expressions, such as x + y, x + y, (x + y) * y, x ^ y, x && y etc.
We need to consider different operations and precedence. To solve this problem, we wrote a function "expression_parse()" specific to parse expressions. First it checks '()' or exponentiation and use recursion to do the calculation inside '()' first, then it does base operation like +, -, *, /, %, after that it does relation operations and restore the results with boolean signs, at last, it completes the boolean operations, if necessary.

Four extensions:

1. Op-equals
2. Relational operations
3. Boolean operations
4. Comments

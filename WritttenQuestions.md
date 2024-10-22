### Question 3

Capture-avoiding substitution is a method used to replace a variable in a mathematical expression without changing its meaning. Imagine you have a formula with placeholders, and you want to swap one placeholder for another value. If you aren’t careful, some parts of the formula might accidentally change meaning because the new value might clash with an existing one. To avoid this, the substitution is done carefully, sometimes renaming other parts, so everything stays clear and correct.

### Question 4

No, you do not always get the expected result in lambda calculus. Not all computations reduce to normal form; some, like the omega combinator, can result in infinite loops and never simplify. While many expressions do reduce to a final form, some expressions will continue expanding indefinitely.


### Question 5

The smallest lambda expression that does not reduce to normal form is called the omega combinator. It looks like this: `(λx. x x) (λx. x x)`. When you try to reduce it, it infinitely applies itself, leading to an endless loop of expansion. As a result, this expression never reaches a final, simplified form, which is why it does not have a normal form.

### Question 2

In lambda calculus, expressions are evaluated by applying functions to arguments.  For this to happen, functions and arguments need to be grouped in pairs.  This is why "a b c d" reduces to "(((a b) c) d)", as it allows for the application of a onto b, c on to the result of that application, and finally d on to the result of the previous applications.  "(a)" reduces to "a" since there are no applications happening.  Since there is no grouping required, the parentheses are dropped.

### Question 3

Capture-avoiding substitution is a method used to replace a variable in a mathematical expression without changing its meaning. Imagine you have a formula with placeholders, and you want to swap one placeholder for another value. If you aren’t careful, some parts of the formula might accidentally change meaning because the new value might clash with an existing one. To avoid this, the substitution is done carefully, sometimes renaming other parts, so everything stays clear and correct.

### Question 4

No, you do not always get the expected result in lambda calculus. Not all computations reduce to normal form; some, like the omega combinator, can result in infinite loops and never simplify. While many expressions do reduce to a final form, some expressions will continue expanding indefinitely.


### Question 5

The smallest lambda expression that does not reduce to normal form is called the omega combinator. It looks like this: `(λx. x x) (λx. x x)`. When you try to reduce it, it infinitely applies itself, leading to an endless loop of expansion. As a result, this expression never reaches a final, simplified form, which is why it does not have a normal form.

### Question 7

((\m.\n. m n) (\f.\x. f (f x))) (\f.\x. f (f (f x)))

((\Var1. (\f.\x. f (f x)) Var1) ) (\f.\x. f (f (f x)))

((\Var2.(\Var4.(Var2 (Var2 Var4)))) (\f.(\x.(f (f (f x))))))

(\Var5.((\f.(\x.(f (f (f x))))) ((\f.(\x.(f (f (f x))))) Var5)))

### Question 8

(12) [ EVALUATION ] (((\m.(\n.(m n))) (\f.(\x.(f (f x))))) (\f.(\x.(f (f (f x))))))
        (40) [ EVALUATION ] ((\m.(\n.(m n))) (\f.(\x.(f (f x)))))
                (40) [ EVALUATION ] (\m.(\n.(m n)))
                        (50) [ EVALUATION ] (\n.(m n))
                                (50) [ EVALUATION ] (m n)
                                        (40) [ EVALUATION ] m
                (44) [ EVALUATION ] (\f.(\x.(f (f x))))
                        (50) [ EVALUATION ] (\x.(f (f x)))
                                (50) [ EVALUATION ] (f (f x))
                                        (40) [ EVALUATION ] f
        (45) [ SUBSTITUTION ] (\n.(m n))
                (84) [ SUBSTITUTION ] (m n)
                        (86) [ SUBSTITUTION ] m
                        (86) [ SUBSTITUTION ] n
                (84) [ SUBSTITUTION ] (m Var1)
                        (86) [ SUBSTITUTION ] m
                        (86) [ SUBSTITUTION ] Var1
                (46) [ EVALUATION ] (\Var1.((\f.(\x.(f (f x)))) Var1))
                        (50) [ EVALUATION ] ((\f.(\x.(f (f x)))) Var1)
                                (40) [ EVALUATION ] (\f.(\x.(f (f x))))
                                        (50) [ EVALUATION ] (\x.(f (f x)))
                                                (50) [ EVALUATION ] (f (f x))
                                                        (40) [ EVALUATION ] f
                                (44) [ EVALUATION ] Var1
                        (45) [ SUBSTITUTION ] (\x.(f (f x)))
                                (84) [ SUBSTITUTION ] (f (f x))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f x)
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] x
                                (84) [ SUBSTITUTION ] (f (f Var2))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f Var2)
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] Var2
                                (46) [ EVALUATION ] (\Var2.(Var1 (Var1 Var2)))
                                        (50) [ EVALUATION ] (Var1 (Var1 Var2))
                                                (40) [ EVALUATION ] Var1
        (44) [ EVALUATION ] (\f.(\x.(f (f (f x)))))
                (50) [ EVALUATION ] (\x.(f (f (f x))))
                        (50) [ EVALUATION ] (f (f (f x)))
                                (40) [ EVALUATION ] f
(45) [ SUBSTITUTION ] (\Var2.(Var1 (Var1 Var2)))
        (84) [ SUBSTITUTION ] (Var1 (Var1 Var2))
                (86) [ SUBSTITUTION ] Var1
                (86) [ SUBSTITUTION ] (Var1 Var2)
                        (86) [ SUBSTITUTION ] Var1
                        (86) [ SUBSTITUTION ] Var2
        (84) [ SUBSTITUTION ] (Var1 (Var1 Var3))
                (86) [ SUBSTITUTION ] Var1
                (86) [ SUBSTITUTION ] (Var1 Var3)
                        (86) [ SUBSTITUTION ] Var1
                        (86) [ SUBSTITUTION ] Var3
        (46) [ EVALUATION ] (\Var3.((\f.(\x.(f (f (f x))))) ((\f.(\x.(f (f (f x))))) Var3)))
                (50) [ EVALUATION ] ((\f.(\x.(f (f (f x))))) ((\f.(\x.(f (f (f x))))) Var3))
                        (40) [ EVALUATION ] (\f.(\x.(f (f (f x)))))
                                (50) [ EVALUATION ] (\x.(f (f (f x))))
                                        (50) [ EVALUATION ] (f (f (f x)))
                                                (40) [ EVALUATION ] f
                        (44) [ EVALUATION ] ((\f.(\x.(f (f (f x))))) Var3)
                                (40) [ EVALUATION ] (\f.(\x.(f (f (f x)))))
                                        (50) [ EVALUATION ] (\x.(f (f (f x))))
                                                (50) [ EVALUATION ] (f (f (f x)))
                                                        (40) [ EVALUATION ] f
                                (44) [ EVALUATION ] Var3
                        (45) [ SUBSTITUTION ] (\x.(f (f (f x))))
                                (84) [ SUBSTITUTION ] (f (f (f x)))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f (f x))
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] (f x)
                                                        (86) [ SUBSTITUTION ] f
                                                        (86) [ SUBSTITUTION ] x
                                (84) [ SUBSTITUTION ] (f (f (f Var4)))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f (f Var4))
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] (f Var4)
                                                        (86) [ SUBSTITUTION ] f
                                                        (86) [ SUBSTITUTION ] Var4
                                (46) [ EVALUATION ] (\Var4.(Var3 (Var3 (Var3 Var4))))
                                        (50) [ EVALUATION ] (Var3 (Var3 (Var3 Var4)))
                                                (40) [ EVALUATION ] Var3
                (45) [ SUBSTITUTION ] (\x.(f (f (f x))))
                        (84) [ SUBSTITUTION ] (f (f (f x)))
                                (86) [ SUBSTITUTION ] f
                                (86) [ SUBSTITUTION ] (f (f x))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f x)
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] x
                        (84) [ SUBSTITUTION ] (f (f (f Var5)))
                                (86) [ SUBSTITUTION ] f
                                (86) [ SUBSTITUTION ] (f (f Var5))
                                        (86) [ SUBSTITUTION ] f
                                        (86) [ SUBSTITUTION ] (f Var5)
                                                (86) [ SUBSTITUTION ] f
                                                (86) [ SUBSTITUTION ] Var5
                        (46) [ EVALUATION ] (\Var5.((\Var4.(Var3 (Var3 (Var3 Var4)))) ((\Var4.(Var3 (Var3 (Var3 Var4)))) ((\Var4.(Var3 (Var3 (Var3 Var4)))) Var5))))
                                (50) [ EVALUATION ] ((\Var4.(Var3 (Var3 (Var3 Var4)))) ((\Var4.(Var3 (Var3 (Var3 Var4)))) ((\Var4.(Var3 (Var3 (Var3 Var4)))) Var5)))
                                        (40) [ EVALUATION ] (\Var4.(Var3 (Var3 (Var3 Var4))))
                                                (50) [ EVALUATION ] (Var3 (Var3 (Var3 Var4)))
                                                        (40) [ EVALUATION ] Var3
                                        (44) [ EVALUATION ] ((\Var4.(Var3 (Var3 (Var3 Var4)))) ((\Var4.(Var3 (Var3 (Var3 Var4)))) Var5))
                                                (40) [ EVALUATION ] (\Var4.(Var3 (Var3 (Var3 Var4))))
                                                        (50) [ EVALUATION ] (Var3 (Var3 (Var3 Var4)))
                                                                (40) [ EVALUATION ] Var3
                                                (44) [ EVALUATION ] ((\Var4.(Var3 (Var3 (Var3 Var4)))) Var5)
                                                        (40) [ EVALUATION ] (\Var4.(Var3 (Var3 (Var3 Var4))))
                                                                (50) [ EVALUATION ] (Var3 (Var3 (Var3 Var4)))
                                                                        (40) [ EVALUATION ] Var3
                                                        (44) [ EVALUATION ] Var5
                                                (45) [ SUBSTITUTION ] (Var3 (Var3 (Var3 Var4)))
                                                        (86) [ SUBSTITUTION ] Var3
                                                        (86) [ SUBSTITUTION ] (Var3 (Var3 Var4))
                                                                (86) [ SUBSTITUTION ] Var3
                                                                (86) [ SUBSTITUTION ] (Var3 Var4)
                                                                        (86) [ SUBSTITUTION ] Var3
                                                                        (86) [ SUBSTITUTION ] Var4
                                                        (46) [ EVALUATION ] (Var3 (Var3 (Var3 Var5)))
                                                                (40) [ EVALUATION ] Var3
                                        (45) [ SUBSTITUTION ] (Var3 (Var3 (Var3 Var4)))
                                                (86) [ SUBSTITUTION ] Var3
                                                (86) [ SUBSTITUTION ] (Var3 (Var3 Var4))
                                                        (86) [ SUBSTITUTION ] Var3
                                                        (86) [ SUBSTITUTION ] (Var3 Var4)
                                                                (86) [ SUBSTITUTION ] Var3
                                                                (86) [ SUBSTITUTION ] Var4
                                                (46) [ EVALUATION ] (Var3 (Var3 (Var3 (Var3 (Var3 (Var3 Var5))))))
                                                        (40) [ EVALUATION ] Var3
                                (45) [ SUBSTITUTION ] (Var3 (Var3 (Var3 Var4)))
                                        (86) [ SUBSTITUTION ] Var3
                                        (86) [ SUBSTITUTION ] (Var3 (Var3 Var4))
                                                (86) [ SUBSTITUTION ] Var3
                                                (86) [ SUBSTITUTION ] (Var3 Var4)
                                                        (86) [ SUBSTITUTION ] Var3
                                                        (86) [ SUBSTITUTION ] Var4
                                        (46) [ EVALUATION ] (Var3 (Var3 (Var3 (Var3 (Var3 (Var3 (Var3 (Var3 (Var3 Var5)))))))))
                                                (40) [ EVALUATION ] Var3
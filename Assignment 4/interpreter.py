import sys
from lark import Lark, Transformer, Tree
import lark
import os
from colorama import Fore, Style

#print(f"Python version: {sys.version}")
#print(f"Lark version: {lark.__version__}")

#  run/execute/interpret source code
def interpret(source_code):
    cst = parser.parse(source_code)
    ast = LambdaCalculusTransformer().transform(cst)
    result = evaluate(ast)
    
    print(Fore.GREEN + "\nPRE-OPERATIONS RESULT (Normalized AST)\n"); print(result); print("\n" + Style.RESET_ALL)
    result2 = evaluate2(result)
    print(Fore.GREEN + f"\nPOST-OPERATIONS RESULT\n{result2}\n" + Style.RESET_ALL)
    print(Fore.GREEN + "\nPOST-OPERATIONS RESULT\n"); print(result2); print("\n" + Style.RESET_ALL)
    return result2

# convert concrete syntax to CST
parser = Lark(open(r"grammar.lark").read(), parser='lalr')

# convert CST to AST
class LambdaCalculusTransformer(Transformer):
    def lam(self, args):
        name, body = args
        return ('lam', str(name), body)
    # def NUMBER(self, args):
    #     return 'num', float(args[0])
    def app(self, args):
        new_args = [(arg.data, arg.children[0]) if isinstance(arg, Tree) and arg.data == 'int' else arg for arg in args]
        return ('app', *new_args)

    def var(self, args):
        token, = args
        return ('var', str(token))
    
    def number(self, args):
        token, = args
        return float(token)
    
    def plus(self, args):
        return ('plus', ('number', args[0]), ('number', args[1]))

    def minus(self, args):
        return ('minus', ('number', args[0]), ('number', args[1]))
    
    def mul(self, args):
        return ('mul', ('number', args[0]), ('number', args[1]))
    
    def div(self, args):
        return ('div', ('number', args[0]), ('number', args[1]))

    def neg(self, args):
        return ('neg', ('number', args[0]))
    
    def if_(self, args):
        return ('if_', ('exp', args[0]), ('exp', args[1]), ('exp', args[2]))
    
    def leq(self, args):
        # Handles: exp <= exp
        return ('leq', ('exp', args[0]), ('exp', args[1]))
    
    def eq(self, args):
        # Handles: exp == exp
        return ('eq', ('exp', args[0]), ('exp', args[1]))
    
    def let(self, args):
        # Handles: let NAME = exp in exp
        name, expr1, expr2 = args
        return ('let', ("var", str(name)), ("exp", expr1), ("exp", expr2))
    
    def rec(self, args):
        # Handles: letrec NAME = exp in exp
        name, expr1, expr2 = args
        return ('letrec', ("var", str(name)), ("exp", expr1), ("exp", expr2))
    
    def fix(self, args):
        # Handles: fix exp
        return ('fix', ('exp', args[0]))
    

    def NAME(self, token):
        return str(token)
    
    # def NUMBER(self, token):
    #     return float(token)

def evaluate(tree, depth: int = 0):
    print(f"{'\t' * depth}[ EVAL-1 ] {tree}")
    if isinstance(tree, (int, float, str)):
        result = tree
    elif isinstance(tree, Tree):
        result = evaluate((tree.data, *tree.children), depth + 1)
    elif tree[0] == 'app':
        print(f"{'\t' * depth}[ APP ] {tree[1]}")
        e1 = evaluate(tree[1])
        print(f"{'\t' * depth}[ E1-RES ] {e1}")
        if e1[0] == 'lam':
            print(f"{'\t' * depth}[ LAM POST E1 ]")
            body = e1[2]
            name = e1[1]
            argument = evaluate(tree[2], depth + 1)
            rhs = substitute(body, name, argument, depth)
            result = evaluate(rhs, depth + 1)
            print(f"{'\t' * depth}[ APP-LAM-RES ] {result}")
        else:
            result = ('app', e1, tree[2])
            print(f"{'\t' * depth}[ NON-LAM-APP-RES ] {result}")
    elif tree[0] == 'lam':
        print(f"{'\t' * depth}[ NON-APP-LAM ]")
        body = evaluate(tree[2], depth + 1)
        result = ('lam', tree[1], body)
        print(f"{'\t' * depth}[ NON-APP-LAM-RES ] {result}")
    else:
        result = tree
        print(f"{'\t' * depth}[ NO-CHANGE-RES ] {result}")
    return result

def evaluate2(tree, depth = 0):
    print(f"{'\t' * depth}[ EVAL-2 ] {tree}")
    if isinstance(tree, (int, float, str)):
        result = tree
    elif isinstance(tree, Tree):
        result = evaluate((tree.data, *tree.children), depth + 1)
    elif tree[0] == 'app':
        print(f"{'\t' * depth}[ EVAL-2-APP ]")
        result = evaluate2(evaluate(tree, depth + 1), depth + 1)
        print(f"{'\t' * depth}[ EVAL-2-APP-RES ] {result}")
    elif tree[0] == 'plus':
        print(f"{'\t' * depth}[ PLUS ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) + evaluate2(tree[2], depth + 1)
        print(f"{'\t' * depth}[ PLUS-RESULT ] {result}")
    elif tree[0] == 'minus':
        print(f"{'\t' * depth}[ MINUS ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) - evaluate2(tree[2], depth + 1)
        print(f"{'\t' * depth}[ MINUS-RESULT ] {result}")
    elif tree[0] == 'mul':
        print(f"{'\t' * depth}[ MUL ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) * evaluate2(tree[2], depth + 1)
        print(f"{'\t' * depth}[ MUL-RESULT ] {result}")
    elif tree[0] == 'div':
        print(f"{'\t' * depth}[ DIV ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) / evaluate2(tree[2], depth + 1)
        print(f"{'\t' * depth}[ DIV-RESULT ] {result}")
    elif tree[0] == 'leq':
        result = evaluate2(tree[1], depth + 1) <= evaluate2(tree[2], depth + 1)
    elif tree[0] == 'eq':
        result = evaluate2(tree[1], depth + 1) == evaluate2(tree[2], depth + 1)
    elif tree[0] == 'number':
        result = evaluate2(tree[1], depth + 1)
    elif tree[0] == 'neg':
        print(f"{'\t' * depth}[ NEG ] {tree[1]}")
        result = -evaluate2(tree[1], depth + 1)
        print(f"{'\t' * depth}[ NEG-RESULT ] {result}")
    elif tree[0] == "if_":
        res_1 = evaluate2(tree[1], depth + 1)
        if not (res_1 == 0):
            result = evaluate2(tree[2], depth + 1)
        else:
            result = evaluate2(tree[3], depth + 1)
    elif tree[0] == "let":      # named var substitution
        _, (name_type, name), (_, expr1), (_, expr2) = tree
        value = evaluate2(expr1, depth + 1)
        substituted_expr2 = substitute(expr2, name, value, depth + 1)
        result = evaluate2(substituted_expr2, depth + 1)
    elif tree[0] == "rec":      # rec NAME = exp in exp, run this recursively
        _, (name_type, name), (_, expr1), (_, expr2) = tree
        # Substitute the variable itself (recursive definition)
        recursive_expr = substitute(expr1, name, ('fix', ('exp', expr1)), depth + 1)
        substituted_expr2 = substitute(expr2, name, recursive_expr, depth + 1)
        result = evaluate2(substituted_expr2, depth + 1)
    elif tree[0] == "fix":
        func = evaluate2(tree[1], depth + 1)
        if func[0] == 'lam':  # Ensure `func` is a lambda (should it be an app and self apply???)
            _, param, body = func
            substituted_body = substitute(body, param, ('fix', ('exp', func)), depth + 1)
            result = evaluate2(substituted_body, depth + 1)
        else:
            raise ValueError(f"Expected a lambda function in 'fix', got {func}")
        # result = evaluate2(tree[1], depth + 1) # this substitutes for a fixed point operator thing
    else:
        result = tree
        print(f"{'\t' * depth}[ NO-CHANGE-RES ] {result}")
    return result

# generate a fresh name 
# needed eg for \y.x [y/x] --> \z.y where z is a fresh name)
class NameGenerator:
    def __init__(self):
        self.counter = 0

    def generate(self):
        self.counter += 1
        # user defined names start with lower case (see the grammar), thus 'Var' is fresh
        return 'Var' + str(self.counter)

name_generator = NameGenerator()

# for beta reduction (capture-avoiding substitution)
# 'replacement' for 'name' in 'tree'
def substitute(tree, name, replacement, depth = 0):
    # tree [replacement/name] = tree with all instances of 'name' replaced by 'replacement'
    print(f"{'\t' * depth}[ SUB ] {replacement} for {name} in {tree}")
    if tree[0] == 'var':
        if tree[1] == name:
            result = replacement # n [r/n] --> r
            print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
        else:
            result = tree # x [r/n] --> x
            print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
    elif tree[0] == 'lam':
        if tree[1] == name:
            result = tree # \n.e [r/n] --> \n.e
            print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
        else:
            fresh_name = name_generator.generate()
            result = ('lam', fresh_name, substitute(substitute(tree[2], tree[1], ('var', fresh_name), depth + 1), name, replacement, depth + 1))
            print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
            # \x.e [r/n] --> (\fresh.(e[fresh/x])) [r/n]
    elif tree[0] == 'app':
        result = ('app', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'plus':
        result = ('plus', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'mul':
        result = ('mul', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'number':
        if isinstance(tree[1], (float, int)):
            result = ('number', tree[1])
            print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
        result = ('number', substitute(tree[1], name, replacement, depth + 1))
        print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'neg':
        result = tree
        print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'if':
        result = ('if', substitute(tree[1], name, replacement),
                        substitute(tree[2], name, replacement),
                        substitute(tree[3], name, replacement))
        return result
    elif tree[0] == 'leq':
        result = (tree[0], substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        return result
    elif tree[0] == 'eq':
        result = (tree[0], substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        return result
    elif tree[0] == 'let':
        result = ('let', tree[1], substitute(tree[2], name, replacement), substitute(tree[3], name, replacement))
        return result
    elif tree[0] == 'rec':
        result = ('rec', tree[1], substitute(tree[2], name, replacement), substitute(tree[3], name, replacement))
        return result
    elif tree[0] == 'fix':
        result = (tree[0], substitute(tree[1], name, replacement))
        return result
    else:
        raise Exception('Unknown tree', tree)

def linearize(ast):
    if isinstance(ast, (int, float, str)):
        return ast
    if ast[0] == 'var':
        return ast[1]
    elif ast[0] == 'lam':
        return "(" + "\\" + ast[1] + "." + linearize(ast[2]) + ")"
    elif ast[0] == 'app':
        return "(" + linearize(ast[1]) + " " + linearize(ast[2]) + ")"
    else:
        return ast

def main():
    import sys
    if len(sys.argv) != 2:
        #print("Usage: python interpreter.py <filename or expression>", file=sys.stderr)
        # sys.exit(1)
        pass

    # input_arg = sys.argv[1]
    input_arg = r"test.lc"

    if os.path.isfile(input_arg):
        # If the input is a valid file path, read from the file
        with open(input_arg, 'r') as file:
            expression = file.read()
    else:
        # Otherwise, treat the input as a direct expression
        expression = input_arg

    result = interpret(expression)
    final_result = f"\033[95m{'FINAL RESULT: ' + str(result)}\033[0m"
    print(final_result)

if __name__ == "__main__":
    main()

import sys
from lark import Lark, Transformer, Tree
import lark
import os
from colorama import Fore, Style

#if(log): print(f"Python version: {sys.version}")
#if(log): print(f"Lark version: {lark.__version__}")

#  run/execute/interpret source code
def interpret(source_code):
    cst = parser.parse(source_code)
    ast = LambdaCalculusTransformer().transform(cst)
    result = evaluate(ast)
    if(log): print(Fore.GREEN + f"\nPRE-OPERATIONS RESULT (Normalized AST)\n{result}\n" + Style.RESET_ALL)
    result2 = evaluate2(result)
    if(log): print(Fore.GREEN + f"\nPOST-OPERATIONS RESULT\n{result2}\n" + Style.RESET_ALL)
    return result2

debug = True
log = True

# convert concrete syntax to CST
if (debug): parser = Lark(open(r"grammar.lark").read(), parser='lalr')
else: parser = Lark(open(r"grammar.lark").read(), parser='lalr')

# convert CST to AST
class LambdaCalculusTransformer(Transformer):
    def lam(self, args):
        name, body = args
        return ('lam', str(name), body)
    # def NUMBER(self, args):
    #     return 'num', float(args[0])
    def app(self, args):
        print(args)
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

    def NAME(self, token):
        return str(token)
    
    def let(self, args):
        print("TESTING")
        print(args[1])
        print(args[2])
        return ('let', args[0], ('var', args[1]), ('var',args[2]))

    def rec(self, args):
        return ('rec', args[0], ('var', args[1]), ('var', args[2]))

    def fix(self, args):
        return ('fix', ('var', args[0]))

    def if_(self, args):
        print("IF", args)
        return ('if', ('var', args[0]), ('var', args[1]), ('var', args[2]))

    def leq(self, args):
        return ('leq', ('var', args[0]), ('var', args[1]))

    def eq(self, args):
        return ('eq', ('var', args[0]), ('var', args[1]))
    
    # def NUMBER(self, token):
    #     return float(token)

def evaluate(tree, depth: int = 0):
    if(log): print(f"{'\t' * depth}[ EVAL-1 ] {tree}")
    if isinstance(tree, (int, float, str)):
        result = tree
    elif isinstance(tree, Tree):
        result = evaluate((tree.data, *tree.children), depth + 1)
    elif tree[0] == 'app':
        if(log): print(f"{'\t' * depth}[ APP ] {tree[1]}")
        e1 = evaluate(tree[1])
        if(log): print(f"{'\t' * depth}[ E1-RES ] {e1}")
        if e1[0] == 'lam':
            if(log): print(f"{'\t' * depth}[ LAM POST E1 ]")
            body = e1[2]
            name = e1[1]
            argument = evaluate(tree[2], depth + 1)
            rhs = substitute(body, name, argument, depth)
            result = evaluate(rhs, depth + 1)
            if(log): print(f"{'\t' * depth}[ APP-LAM-RES ] {result}")
        else:
            result = ('app', e1, tree[2])
            if(log): print(f"{'\t' * depth}[ NON-LAM-APP-RES ] {result}")
    elif tree[0] == 'lam':
        if(log): print(f"{'\t' * depth}[ NON-APP-LAM ]")
        body = evaluate(tree[2], depth + 1)
        result = ('lam', tree[1], body)
        if(log): print(f"{'\t' * depth}[ NON-APP-LAM-RES ] {result}")
    else:
        result = tree
        if(log): print(f"{'\t' * depth}[ NO-CHANGE-RES ] {result}")
    return result

def evaluate2(tree, depth = 0):
    if(log): print(f"{'\t' * depth}[ EVAL-2 ] {tree}")
    if isinstance(tree, (int, float, str)):
        result = tree
    elif isinstance(tree, Tree):
        result = evaluate((tree.data, *tree.children), depth + 1)
    elif tree[0] == 'app':
        if(log): print(f"{'\t' * depth}[ EVAL-2-APP ]")
        result = evaluate2(evaluate(tree, depth + 1), depth + 1)
        if(log): print(f"{'\t' * depth}[ EVAL-2-APP-RES ] {result}")
    elif tree[0] == 'var':
        result = evaluate2(tree[1])
    elif tree[0] == 'plus':
        if(log): print(f"{'\t' * depth}[ PLUS ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) + evaluate2(tree[2], depth + 1)
        if(log): print(f"{'\t' * depth}[ PLUS-RESULT ] {result}")
    elif tree[0] == 'minus':
        if(log): print(f"{'\t' * depth}[ MINUS ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) - evaluate2(tree[2], depth + 1)
        if(log): print(f"{'\t' * depth}[ MINUS-RESULT ] {result}")
    elif tree[0] == 'if':
        _if = evaluate2(tree[1])
        print(str(tree[1]) + "    IF")
        _else = evaluate2(tree[3])
        print(tree)
        _then = evaluate2(tree[2])
        if _if == 0.0:  # False
            
            result = ('var', _else)
        else:  # true
            result = ('var', _then)
    elif tree[0] == 'mul':
        if(log): print(f"{'\t' * depth}[ MUL ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) * evaluate2(tree[2], depth + 1)
        if(log): print(f"{'\t' * depth}[ MUL-RESULT ] {result}")
    elif tree[0] == 'div':
        if(log): print(f"{'\t' * depth}[ DIV ] {tree[1]} + {tree[2]}")
        result = evaluate2(tree[1], depth + 1) / evaluate2(tree[2], depth + 1)
        if(log): print(f"{'\t' * depth}[ DIV-RESULT ] {result}")
    elif tree[0] == 'number':
        result = evaluate2(tree[1], depth + 1)
    elif tree[0] == 'eq':
        result = (float)(tree[1] == tree[2][1])
    elif tree[0] == 'leq':
        result = (float)(tree[1][1] <= tree[2][1])
    elif tree[0] == 'let':
        print("LETTING")
        print(tree)
        print(tree[2])
        print(tree[3])

        ## SPEIAL TEMP CASE FOR LAME WHEN  ('let', 'g', ('lam', 'Var1', ('plus', ('number', 'Var1'), ('number', 1.0)))

        result = evaluate2(substitute(tree[3][1], tree[1], (tree[2][1])))
    elif tree[0] == 'neg':
        if(log): print(f"{'\t' * depth}[ NEG ] {tree[1]}")
        result = -evaluate2(tree[1], depth + 1)
        if(log): print(f"{'\t' * depth}[ NEG-RESULT ] {result}")
    else:
        result = tree
        if(log): print(f"{'\t' * depth}[ NO-CHANGE-RES ] {result}")
    return result

def evaluate_condition(tree):
    if tree[0] == 'var':
        return tree[1] == 1.0
    elif tree[0] == 'eq':
        return tree[1] == tree[2]
    elif tree[0] == 'leq':
        return tree[1] <= tree[2]
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
    print("tree: " + str(tree))
    print("replacement: " + str(replacement))
    print("name: " + str(name))
    # tree [replacement/name] = tree with all instances of 'name' replaced by 'replacement'
    if(log): print(f"{'\t' * depth}[ SUB ] {replacement} for {name} in {tree}")
    if(isinstance(tree, float)):
        return tree
    if (tree == replacement or tree == name): result = tree
    if tree[0] == 'var':
        if tree[1] == name:            
            result = replacement # n [r/n] --> r
            if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")

            return result
        elif not isinstance(tree[1], float):
            result = substitute(tree[1],name,replacement)
        else:
            result = tree # x [r/n] --> x
            if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
            print("RESULTING")
            print(result)
            return result
    elif tree[0] == 'lam':
        if tree[1] == name:
            result = tree # \n.e [r/n] --> \n.e
            if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
        else:
            fresh_name = name_generator.generate()
            result = ('lam', fresh_name, substitute(substitute(tree[2], tree[1], ('var', fresh_name), depth + 1), name, replacement, depth + 1))
            if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
            # \x.e [r/n] --> (\fresh.(e[fresh/x])) [r/n]
    elif tree[0] == 'app':
        result = ('app', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'let':
        result = ('let',tree[1], substitute(tree[2], name, replacement, depth + 1), substitute(tree[3], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'plus':
        result = ('plus', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'if':
        print(substitute(tree[1], name, replacement, depth + 1))
        result = ('if', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1), substitute(tree[3], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'eq':
        
        result = ('eq', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")

        return result
    elif tree[0] == 'leq':
        result = ('leq', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
    elif tree[0] == 'mul':
        result = ('mul', substitute(tree[1], name, replacement, depth + 1), substitute(tree[2], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'number':
        if isinstance(tree[1], (float, int)):
            result = ('number', tree[1])
            if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
            return result
        result = ('number', substitute(tree[1], name, replacement, depth + 1))
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    elif tree[0] == 'neg':
        result = tree
        if(log): print(f"{'\t' * depth}[ SUB-RES ] {result}")
        return result
    else:
        result = tree
    print(tree)
    return result
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
        #if(log): print("Usage: python interpreter.py <filename or expression>", file=sys.stderr)
        # sys.exit(1)
        pass

    # input_arg = sys.argv[1]
    if (debug): input_arg = r"test.lc"
    else: input_arg = r"test.lc"

    if os.path.isfile(input_arg):
        # If the input is a valid file path, read from the file
        with open(input_arg, 'r') as file:
            expression = file.read()
    else:
        # Otherwise, treat the input as a direct expression
        expression = input_arg

    result = interpret(expression)
    final_result = f"\033[95m{'FINAL RESULT: ' + str(result)}\033[0m"
    if(log): print(final_result)

if __name__ == "__main__":
    main()

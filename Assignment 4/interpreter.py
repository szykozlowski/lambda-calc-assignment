import sys
from lark import Lark, Transformer, Tree
import lark
import os

#print(f"Python version: {sys.version}")
#print(f"Lark version: {lark.__version__}")

#  run/execute/interpret source code
def interpret(source_code):
    cst = parser.parse(source_code)
    ast = LambdaCalculusTransformer().transform(cst)
    result = evaluate(ast)
    result2 = evaluate2(result)
    print(result)
    print(result2)
    # result = linearize(result)
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

    def NAME(self, token):
        return str(token)
    
    # def NUMBER(self, token):
    #     return float(token)

def evaluate(tree):
    print(tree)
    if isinstance(tree, (int, float, str)):
        return tree
    if isinstance(tree, Tree):
        return evaluate((tree.data, *tree.children))
    if tree[0] == 'app':
        print(f"UNDER APP : {tree}")
        print(tree[1])
        e1 = evaluate(tree[1])
        print("gothisfar")
        print(e1)
        print(f"\t{e1}")
        if e1[0] == 'lam':
            print("SUB TIME")
            body = e1[2]
            name = e1[1]
            argument = evaluate(tree[2])
            rhs = substitute(body, name, argument)
            result = evaluate(rhs) 
        else:
            result = ('app', e1, tree[2])
    elif tree[0] == 'lam':
        body = evaluate(tree[2])
        result = ('lam', tree[1], body)
    # elif tree[0] == 'plus':
    #     print(f"PLUSING: {tree}")
    #     result = evaluate(tree[1]) + evaluate(tree[2])
    # elif tree[0] == 'minus':
    #     result = evaluate(tree[1]) - evaluate(tree[2])
    # elif tree[0] == 'mul':
    #     result = evaluate(tree[1]) * evaluate(tree[2])
    # elif tree[0] == 'div':
    #     result = evaluate(tree[1]) / evaluate(tree[2])
    # elif tree[0] == 'number':
    #     return evaluate(tree[1])
    # elif tree[0] == 'neg':
    #     return -evaluate(tree[1])
    else:
        result = tree
    return result

def evaluate2(tree):
    print(tree)
    if isinstance(tree, (int, float, str)):
        return tree
    if isinstance(tree, Tree):
        return evaluate((tree.data, *tree.children))

    if tree[0] == 'plus':
        print(f"PLUSING: {tree}")
        result = evaluate2(tree[1]) + evaluate2(tree[2])
    elif tree[0] == 'minus':
        result = evaluate2(tree[1]) - evaluate2(tree[2])
    elif tree[0] == 'mul':
        result = evaluate2(tree[1]) * evaluate2(tree[2])
    elif tree[0] == 'div':
        result = evaluate2(tree[1]) / evaluate2(tree[2])
    elif tree[0] == 'number':
        return evaluate2(tree[1])
    elif tree[0] == 'neg':
        return -evaluate2(tree[1])
    else:
        result = tree
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
def substitute(tree, name, replacement):
    # tree [replacement/name] = tree with all instances of 'name' replaced by 'replacement'
    print(f"Subbing {replacement} for {name} in {tree}")
    if tree[0] == 'var':
        if tree[1] == name:
            return replacement # n [r/n] --> r
        else:
            return tree # x [r/n] --> x
    elif tree[0] == 'lam':
        if tree[1] == name:
            return tree # \n.e [r/n] --> \n.e
        else:
            fresh_name = name_generator.generate()
            return ('lam', fresh_name, substitute(substitute(tree[2], tree[1], ('var', fresh_name)), name, replacement))
            # \x.e [r/n] --> (\fresh.(e[fresh/x])) [r/n]
    elif tree[0] == 'app':
        return ('app', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'plus':
        return ('plus', substitute(tree[1], name, replacement), substitute(tree[2], name, replacement))
    elif tree[0] == 'number':
        if isinstance(tree[1], (float, int)):
            return ('number', tree[1])
        return ('number', substitute(tree[1], name, replacement))
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
    print(f"\033[95m{result}\033[0m")

if __name__ == "__main__":
    main()

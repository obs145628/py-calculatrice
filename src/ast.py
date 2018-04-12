from .code_parser import ASTNode
import src.code_parser as cp


class IntNode(ASTNode):

    def __init__(self, loc, val):
        ASTNode.__init__(self, 'int', loc)
        self.val = val

class FloatNode(ASTNode):
    def __init__(self, loc, val):
        ASTNode.__init__(self, 'float', loc)
        self.val = val

class StringNode(ASTNode):
    def __init__(self, loc, val):
        ASTNode.__init__(self, 'string', loc)
        self.val = val

class IdNode(ASTNode):
    def __init__(self, loc, val):
        ASTNode.__init__(self, 'id', loc)
        self.val = val

class CallNode(ASTNode):
    def __init__(self, loc, fun, args):
        ASTNode.__init__(self, 'call', loc, [fun] + args)
        self.fun = fun
        self.args = args

class ExpsBlockNode(ASTNode):
    def __init__(self, loc, exps):
        ASTNode.__init__(self, 'exps_block', exps)
        self.exps = exps

class Printer(cp.Visitor):

    def f_int(self, node):
        return str(node.val)

    def f_string(self, node):
        return str(node.val)

    def f_float(self, node):
        return str(node.val)

    def f_id(self, node):
        return str(node.val)

    def f_call(self, node):
        res = self(node.fun) + '('
        for i in range(len(node.args)):
            res += self(node.args[i])
            if i + 1 < len(node.args):
                res += ', '
        return res + ')'


def print_ast(ast):
    p = Printer()
    print(p(ast))
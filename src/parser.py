import src.code_parser as cp
import src.ast as ast



OP_FUNS = {
    '+': '__add__',
    '-': '__sub__',
    '*': '__mul__',
    '/': '__div__',
}

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_token(self, types = None, value = None):
        token = self.lexer.get_token()
        if not self.is_token(token, types, value):
            raise Exception("Invalid token")
        return token

    def peek_token(self, types = None, value = None):
        token = self.lexer.peek_token()
        if not self.is_token(token, types, value):
            return None
        return token

    def is_token(self, token, types = None, value = None):
        if types != None and token.type not in types:
            return False
        if value != None and token.val != value:
            return False
        return True


    def build_ast(self):
        return self.program()

    def program(self):
        return self.statement()

    def statement(self):
        return self.exp()

    def exp(self):
        return self.pred_max()


    def pred_max(self):
        return self.bin_pred2()

    def bin_pred2(self):  #operators + and -

        res = self.bin_pred1()

        while True:

            op = self.peek_token()
            if op.type != cp.TOKEN_OP or (op.val != '+' and op.val != '-'):
                break
            self.get_token()

            right = self.bin_pred1()
            res = ast.CallNode(op.loc, ast.IdNode(op.loc, OP_FUNS[op.val]), [res, right])

        return res


    def bin_pred1(self): #operators * and /

        res = self.un_pred1()

        while True:

            op = self.peek_token()
            if op.type != cp.TOKEN_OP or (op.val != '*' and op.val != '/'):
                break
            self.get_token()

            right = self.un_pred1()
            res = ast.CallNode(op.loc, ast.IdNode(op.loc, OP_FUNS[op.val]), [res, right])

        return res

    def un_pred1(self):  #unary operators + and -

        op = self.peek_token()
        if op.type != cp.TOKEN_OP or (op.val != '+' and op.val != '-'):
            return self.value()
        self.get_token()

        right = self.un_pred1()
        return ast.CallNode(op.loc, ast.IdNode(op.loc, OP_FUNS[op.val]), [right])

    def value(self): #(exp) or litteral or lvalue or lvalue-call
        if self.peek_token([cp.TOKEN_OP], '('):
            return self.value_par()

        if self.peek_token([cp.TOKEN_ID]):
            return self.value_lvalue_start()

        if self.peek_token([cp.TOKEN_INT, cp.TOKEN_REAL,
                            cp.TOKEN_SQSTRING, cp.TOKEN_DQSTRING]):
            return self.value_lit()

        raise Exception("Invalid token")

    def value_par(self): #(exp)
        self.get_token([cp.TOKEN_OP], '(')
        res = self.exp()
        self.get_token([cp.TOKEN_OP], ')')
        return res

    def value_lit(self): #literal (int / float / string)
        token = self.get_token([cp.TOKEN_INT, cp.TOKEN_REAL,
                                cp.TOKEN_SQSTRING, cp.TOKEN_DQSTRING,
                                ])
        if token.type == cp.TOKEN_INT:
            return ast.IntNode(token.loc, token.val)
        elif token.type == cp.TOKEN_REAL:
            return ast.FloatNode(token.loc, token.val)
        elif token.type == cp.TOKEN_SQSTRING or token.type == cp.TOKEN_DQSTRING:
            return ast.StringNode(token.loc, token.val)
        else:
            raise Exception("unreachable")

    def value_lvalue_start(self): #lvalue or lvalue(exps...)
        lval = self.value_lvalue()
        if self.peek_token([cp.TOKEN_OP], '('):
            return self.value_call(lval)
        else:
            return lval



    def value_lvalue(self): #lvalue(exps...) lvalue already parsed
        token = self.get_token([cp.TOKEN_ID])
        return ast.IdNode(token.loc, token.val)

    def value_call(self, lval):
        self.get_token([cp.TOKEN_OP], '(')
        args = []

        while True:
            if self.peek_token([cp.TOKEN_OP], ')'):
                self.get_token()
                break

            if len(args) != 0 and not self.get_token([cp.TOKEN_OP], ','):
                raise Exception('Invalid token: expected `,` or `)`')

            args.append(self.exp())

        return ast.CallNode(lval.loc, lval, args)


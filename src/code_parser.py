import os


####  UTILS  ####


def get_file(val):
    return _files[val]


def is_letter(s):
    return s != None and (s.lower() >= 'a' and s.lower() <= 'z')

def is_digit(s):
    return s != None and s >= '0' and s <= '9'

def is_idchar(s):
    return is_letter(s) or is_digit(s) or s == '_'


class Position:

    def __init__(self, id, line, col):
        self.id = id
        self.line = line
        self.col = col

    def __str__(self):
        return get_file(self.id) + ':' + str(self.line) + ':' + str(self.col)

class Location:

    def __init__(self, begin, end):
        self.id = begin.id
        self.begin = begin
        self.end = end
        assert(begin.id == end.id)

    def __str__(self):
        res = get_file(self.id) + ':'
        if self.begin.line == self.end.line:
            res += str(self.begin.line) + ':' + str(self.begin.col) + '-' + str(self.end.col)
        else:
            res += str(self.begin.line) + ':' + str(self.begin.col) + '-' + str(self.end.line) + ':' +  str(self.end.col)
        return res










### Lexer ###

_files = []
def add_file(name):
    val = len(_files)
    _files.append(name)
    return val




class FileStream:

    def __init__(self, path):
        self.path = path
        self.f = None
        self.id = add_file(os.path.abspath(path))

    def open(self):
        self.f = open(self.path, 'r')

    def close(self):
        self.f.close()

    def getc(self):
        c =  self.f.read(1)
        return None if len(c) == 0 else c
    
class StringStream:

    def __init__(self, s):
        self.s = str(s)
        self.i = None
        self.id = add_file('(string)')

    def open(self):
        self.i = 0

    def close(self):
        self.i = None

    def getc(self):
        if self.i == len(self.s):
            return None
        else:
            c = self.s[self.i]
            self.i += 1
            return c

class InputReader:

    def __init__(self, ins):
        self.ins = ins
        self.line = 1
        self.col = 1
        self.buff = None

    def peekc(self):
        if self.buff != None:
            return self.buff
        self.buff = self._get()
        return self.buff

    def getc(self):
        if self.buff != None:
            res = self.buff
            self.buff = None
        else:
            res = self._get()

        self._update_pos(res)
        return res

    def _get(self):
        c = self.ins.getc()
        if c  == '\n':
            return '\n'
        elif c == None:
            return None
        else:
            return c

    def _update_pos(self, c):
        if c  == '\n':
            self.line += 1
            self.col = 1
        elif c != None:
            self.col += 1

    def pos(self):
        return Position(self.ins.id, self.line, self.col)


TOKEN_EOF = 0
TOKEN_KEYWORD = 1
TOKEN_INT = 2
TOKEN_REAL = 3
TOKEN_SQSTRING = 4
TOKEN_DQSTRING = 5
TOKEN_ID = 6
TOKEN_OP = 7
TOKEN_ERROR = 8

NAMES_TOKENS_ = ["EOF",
    "KEYWORD",
    "INT", "REAL",
    "SQSTRING", "DQSTRING",
    "ID", "OPERATOR",
    "ERROR"]

class Token:

    def __init__(self, loc, type, val = None):
        self.loc = loc
        self.type = type
        self.val = val

    def __str__(self):
        res =  str(self.loc) + ':' + NAMES_TOKENS_[self.type]
        if self.val != None:
            res += ' = <' + str(self.val) + '>'
        return res


class ParserOptions:

    def __init__(self, enable_int, enable_real, enable_sqstring,
                 enable_dqstring, enable_com1, enable_com2,
                 keywords, ops):
        self.enable_int = enable_int
        self.enable_real = enable_real
        self.enable_sqstring = enable_sqstring
        self.enable_dqstring = enable_dqstring
        self.enable_com1 = enable_com1
        self.enable_com2 = enable_com2
        self.keywords = keywords
        self.ops = ops


class Lexer:

    def __init__(self, stream, conf):

        self._stream = InputReader(stream)
        self._stream.ins.open()
        self._conf = conf
        self._tokens = []
        self._tokens_i = 0

        self.errors = []
        
    def peek_token(self):
        while self._tokens_i >= len(self._tokens):
            self._tokens.append(self._read_token())
        return self._tokens[self._tokens_i]

    def get_token(self):
        res = self.peek_token()
        if res.type != TOKEN_EOF:
            self._tokens_i += 1
        return res

    def filter_tokens(self, tokens, str):
        return list(filter(lambda x: x.startswith(str), tokens))

    def _read_token(self):

        self._pass_white()
        c = self._stream.peekc()
        if c == None:
            return self._build_token(self._stream.pos(), self._stream.pos(), TOKEN_EOF)

        if c == '/' and (self._conf.enable_com1 or self._conf.enable_com2):
            begin = self._stream.pos()
            self._stream.getc()
            c = self._stream.peekc()
            if c == '/' and self._conf.enable_com1:
                self._pass_com1()
                return self._read_token()
            if c == '*' and self._conf.enable_com2:
                self._pass_com2()
                return self._read_token()

            end = self._stream.pos()
            if '/' and self._conf.ops:
                return self._build_token(begin, end, TOKEN_OP, '/')
            else:
                return self._error(begin, end, 'Invalid character')



        if len(self.filter_tokens(self._conf.ops, c)) > 0:
           return self._read_operator()

        if is_digit(c):
            return self._read_number()

        if is_idchar(c):
            return self._read_word()

        if c == '\'' and self._conf.enable_sqstring:
            return self._read_string()

        if c == '"' and self._conf.enable_dqstring:
            return self._read_string()


        begin = self._stream.pos()
        self._stream.getc()
        return self._error(begin, self._stream.pos(), 'Invalid character')

    def _read_operator(self):
        pos = [self._stream.pos()]
        str = ""
        ops = self._conf.ops

        while True:
            c = self._stream.peekc()
            if c is None:
                str += '0'
                break
            str += c
            ops = self.filter_tokens(ops, str)
            if len(ops) == 0:
                break
            self._stream.getc()
            pos.append(self._stream.pos())

        str = str[:-1]
        return self._build_operator(str, pos)

    def _read_number(self):
        begin = self._stream.pos()
        is_real = False

        str = ""

        while True:
            c = self._stream.peekc()
            if c == '.' and not is_real:
                is_real = True
            elif is_digit(c):
                pass
            else:
                break

            self._stream.getc()
            str += c

        end = self._stream.pos()

        if is_real:
            if self._conf.enable_real:
                return self._build_token(begin, end, TOKEN_REAL, float(str))
            else:
                return self._error(begin, end, 'Invalid real')
        else:
            if self._conf.enable_int:
                return self._build_token(begin, end, TOKEN_INT, int(str))
            else:
                return self._error(begin, end, 'Invalid integer')

    def _read_word(self):

        str = ""
        begin = self._stream.pos()

        while True:
            c = self._stream.peekc()
            if not is_idchar(c):
                break
            str += c
            self._stream.getc()

        end = self._stream.pos()

        if str in self._conf.keywords:
            return self._build_token(begin, end, TOKEN_KEYWORD, str)
        else:
            return self._build_token(begin, end, TOKEN_ID, str)

    def _read_string(self):

        begin = self._stream.pos()
        delim = self._stream.getc()
        escaped = False
        str = delim

        while True:
            c = self._stream.getc()
            if c == None:
                return self._error(begin, self._stream.pos(), "unfinished string")
            str += c
            if c == delim and not escaped:
                break
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True

        end = self._stream.pos()
        if delim == '\\':
            return self._build_token(begin, end, TOKEN_SQSTRING, str)
        else:
            return self._build_token(begin, end, TOKEN_DQSTRING, str)



    def _build_operator(self, str, pos):

        begin = pos[0]

        while True:
            if str in self._conf.ops:
                break
            str = str[:-1]
            pos = pos[:-1]

        end = pos[-1]
        return self._build_token(begin, end, TOKEN_OP, str)




    def _pass_white(self):
        while True:
            c = self._stream.peekc()
            if c is None or not c.isspace():
                break
            self._stream.getc()

    def _pass_com1(self):
        while True:
            c = self._stream.getc()
            if c == '\n' or c is None:
                return

    def _pass_com2(self):
        end = '*/'
        str = ''

        while True:
            c = self._stream.getc()
            if c == None:
                return

            if c == end[len(str)]:

                str += c
                if len(str) == len(end):
                    return
            else:
                str = ''



    def _build_token(self, begin, end, type, val = None):
        return Token(Location(begin, end), type, val)

    def _error(self, begin, end, mess):
        tok = Token(Location(begin, end), TOKEN_ERROR)
        self.errors.append((mess, tok))
        return tok
    

    


####  Parser  ####









#### AST ####

class ASTNode:

    def __init__(self, node_type, loc, children = []):
        self.node_type = node_type
        self.loc = loc
        self.children = children

    def __str__(self):
        dp = DebugPrint()
        return dp.run(self)

class Visitor:

    def visit(self, node):
        return self._call_visitor(node)

    def __call__(self, node):
        return self.visit(node)

    def _call_visitor(self, node):
        if ('f_' + node.node_type) in dir(self):
            meth = getattr(self, 'f_' + node.node_type)
        else:
            meth = getattr(self, 'f_ast')
        return meth(node)

    def f_ast(self, node):
        raise Exception('f_ast not implemented')


class DebugPrint(Visitor):

    def __init__(self):
        self._res = ""

    def run(self, ast):
        self(ast)
        return self._res

    def f_ast(self, node):
        self._res += str(node.node_type)
        if len(node.children) != 0:
            self._res += '[\n'
            for n in node.children:
                self(n)
                self._res += '\n'
            self._res += ']\n'











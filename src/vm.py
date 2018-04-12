

_ntypes = 0
def add_type():
    global _ntypes
    res = _ntypes
    _ntypes += 1
    return res

TYPE_VOID = add_type()
TYPE_INT = add_type()
TYPE_FLOAT = add_type()
TYPE_STRING = add_type()
TYPE_LVALUE = add_type()
TYPE_FUNCTION = add_type()

class Value:

    def __init__(self, type):
        self.type = type

class ValueVoid(Value):

    def __init__(self):
        Value.__init__(self, TYPE_VOID)


class ValueInt(Value):

    def __init__(self, val):
        Value.__init__(self, TYPE_INT)
        self.val = int(val)


class ValueFloat(Value):

    def __init__(self, val):
        Value.__init__(self, TYPE_FLOAT)
        self.val = float(val)


class ValueString(Value):

    def __init__(self, val):
        Value.__init__(self, TYPE_STRING)
        self.val = str(val)


class ValueLval(Value):

    def __init__(self, val):
        Value.__init__(self, TYPE_LVALUE)
        self.val = str(val)



class VMFunction:

    def __init__(self, native_fun, first_type = None):
        self.native_fun = native_fun
        self.first_type = first_type


_funs = dict()


def declare_fun(name, fun):
    global _funs
    first_type = fun.first_type

    if name not in _funs:
        _funs[name] = (None, dict())
    fun_obj = _funs[name]
    if first_type is None:
        if len(fun_obj[1]) != 0 or fun_obj[0] is not None:
            raise Exception("Can't declare native normal functions: already exists")
        fun_obj[0] = fun
    else:
        if fun_obj[0] is not None:
            raise Exception("Can't declare native special functions: already exists")
        fun_obj[1][first_type] = fun

def get_fun(name, args):
    global _funs

    if name not in _funs:
        return None
    fun_obj = _funs[name]

    if fun_obj[0] is None:
        first_type = args[0].type
        return fun_obj[1][first_type] if first_type in fun_obj[1] else None
    else:
        return fun_obj[0]




class VM:

    def __init__(self):
        self.vars = dict()
        self.funs = dict()

    def load_var(self, name):
        return self.vars[name] if name in self.vars else None

    def store_var(self, name, val):
        self.vars[name] = val

    def clear_var(self, name):
        del self.vars[name]

    def exec_fun(self, name, args):
        fun = get_fun(name, args)
        if fun is None:
            raise Exception("Runtime Error: call to " + name + " failed")
        return fun.native_fun(args)


class FunTypeMatcher:

    def __init__(self, arg_num, funs_dict, fun_default = None):
        self.arg_num = arg_num
        self.funs_dict = funs_dict
        self.fun_default = fun_default

    def __call__(self, args):
        if self.arg_num >= len(args):
            raise Exception('Invalid number of arguments')

        type = args[self.arg_num].type
        if type in self.funs_dict:
            return self.funs_dict[type](args)

        if self.fun_default != None:
            return self.fun_default(args)
        else:
            raise Exception('Invalid types for arguments')
import src.code_parser as cp
import src.vm as vm

class Eval(cp.Visitor):

    def __init__(self):
        self.vm = vm.VM()

    def f_int(self, node):
        return vm.ValueInt(node.val)

    def f_float(self, node):
        return vm.ValueFloat(node.val)

    def f_string(self, node):
        return vm.ValueString(node.val)

    def f_id(self, node):
        return vm.ValueLval(node.val)

    def f_call(self, node):

        name = self(node.fun)
        if name.type != vm.TYPE_LVALUE:
            raise Exception("Call: called object is not an lvalue")
        name = name.val

        args = [self(x) for x in node.args]
        return self.vm.exec_fun(name, args)


def eval(ast):
    v = Eval()
    return v(ast)


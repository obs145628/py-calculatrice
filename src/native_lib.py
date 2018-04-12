import src.vm as vm



def s_add_int_int(a, b):
    return vm.ValueInt(a.val + b.val)

def s_add_int_float(a, b):
    return vm.ValueFloat(a.val + b.val)

def s_sub_int_int(a, b):
    return vm.ValueInt(a.val - b.val)

def s_sub_int_float(a, b):
    return vm.ValueFloat(a.val - b.val)

def s_add_int_int(a, b):
    return vm.ValueInt(a.val + b.val)

def s_add_int_float(a, b):
    return vm.ValueFloat(a.val + b.val)

def s_mul_int_int(a, b):
    return vm.ValueInt(a.val * b.val)

def s_mul_int_float(a, b):
    return vm.ValueFloat(a.val * b.val)

def s_div_int_int(a, b):
    return vm.ValueInt(a.val / b.val)

def s_div_int_float(a, b):
    return vm.ValueFloat(a.val / b.val)

def s_add_int(a):
    return a.val

def s_add_float(a):
    return a

def s_sub_int(a):
    return vm.ValueInt(-a.val)

def s_sub_float(a):
    return vm.ValueFloat(-a.val)
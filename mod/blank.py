call = lambda f, *args: f(f, *args[:-1])

liste_inst = REPLACE_1

buildins = {
    x:eval(x) for x in dir(__builtins__) if x in [z[3] for z in liste_inst]
}
buildins.update({
    "f":lambda x : str((lambda f, *args: f(f, *args[:-1]))(lambda f, nb, total : f(f, nb-1, total * nb) if nb != 1 else total, x, 1, __import__("sys").setrecursionlimit(2**31-1))).strip("0")[-4:]
})

UNKNOWN_INSTRUCTION = lambda  f, cmpt, insts, stack, var_dict : print(f"Error : unknown instruction {insts[cmpt]}")

BINARY_ADD = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__add__(stack.pop(-1))], var_dict]))
BINARY_SUB = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__sub__(stack.pop(-1))], var_dict]))
BINARY_MUL = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__mul__(stack.pop(-1))], var_dict]))
BINARY_DIV = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__truediv__(stack.pop(-1))], var_dict]))
BINARY_POW = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__pow__(stack.pop(-1))], var_dict]))

COMPARE_DIFFERENT = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2) != stack.pop(-1)], var_dict]))
COMPARE_BIGGER    = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2) > stack.pop(-1)], var_dict]))
COMPARE_SMALLER   = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2) < stack.pop(-1)], var_dict]))
COMPARE_EQUAL   = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2) == stack.pop(-1)], var_dict]))

RETURN_VALUE = (lambda f, cmpt, insts, stack, var_dict : [stack.pop(-1), stack, var_dict])
RESUME       = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack, var_dict]))
LOAD_CONST   = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack + [insts[cmpt][3]], var_dict]))
STORE_NAME   = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack, [var_dict.update({insts[cmpt][3]:stack.pop(-1)}), var_dict][1]]))
BUILD_LIST   = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[0:len(stack)-insts[cmpt][3]] + [stack[len(stack)-insts[cmpt][3]:]], var_dict]))
LOAD_NAME    = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack+[var_dict[insts[cmpt][3]]], var_dict]))
BINARY_OP    = (lambda f, cmpt, insts, stack, var_dict : {
    "+" : BINARY_ADD,
    "-" : BINARY_SUB,
    "*" : BINARY_MUL,
    "/" : BINARY_DIV,
    "**" : BINARY_POW,
}.get(insts[cmpt][4], UNKNOWN_INSTRUCTION)(f, cmpt, insts, stack, var_dict))
NOP          = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack, var_dict]))
POP_TOP      = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-1], var_dict]))
LIST_EXTEND  = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, [stack[i] if i != len(stack) - 2 else stack[i]+list(x for x in stack[i+1]) for i in range(len(stack) - 1)], var_dict]))
POP_JUMP_FORWARD_IF_FALSE = (lambda f, cmpt, insts, stack, var_dict : f(*[f, insts.index(*[inst for inst in insts if inst[5] == insts[cmpt][3]]), insts, stack, var_dict]) if not stack.pop() else f(*[f, cmpt+1, insts, stack, var_dict]))
POP_JUMP_BACKWARD_IF_TRUE = (lambda f, cmpt, insts, stack, var_dict : f(*[f, insts.index(*[inst for inst in insts if inst[5] == insts[cmpt][3]]), insts, stack, var_dict]) if stack.pop() else f(*[f, cmpt+1, insts, stack, var_dict]))
PUSH_NULL    = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack + [None], var_dict]))
PRECALL      = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack, var_dict]))
CALL         = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts,stack[:len(stack)-insts[cmpt][2]-2] + [(stack[len(stack)-insts[cmpt][2]-1](*stack[len(stack)-insts[cmpt][2]:]))], var_dict]))
COMPARE_OP    = (lambda f, cmpt, insts, stack, var_dict : {
    "!=" : COMPARE_DIFFERENT,
    ">" : COMPARE_BIGGER,
    "<" : COMPARE_SMALLER,
    "==" : COMPARE_EQUAL,
}.get(insts[cmpt][4], UNKNOWN_INSTRUCTION)(f, cmpt, insts, stack, var_dict))

step = lambda f, cmpt, insts, stack, var_dict : {
    "RETURN_VALUE" : RETURN_VALUE,
    "RESUME" : RESUME,
    "LOAD_CONST" : LOAD_CONST,
    "STORE_NAME" : STORE_NAME,
    "BUILD_LIST" : BUILD_LIST,
    "LOAD_NAME" : LOAD_NAME,
    "BINARY_OP" : BINARY_OP,
    "NOP" : NOP,
    "POP_TOP" : POP_TOP,
    "LIST_EXTEND" : LIST_EXTEND,
    "POP_JUMP_FORWARD_IF_FALSE" : POP_JUMP_FORWARD_IF_FALSE,
    "POP_JUMP_BACKWARD_IF_TRUE" : POP_JUMP_BACKWARD_IF_TRUE,
    "PUSH_NULL" : PUSH_NULL,
    "PRECALL" : PRECALL,
    "CALL" : CALL,
    "COMPARE_OP" : COMPARE_OP,
}.get(insts[cmpt][0], UNKNOWN_INSTRUCTION)(f, cmpt, insts, stack, var_dict)

prog = lambda : call(step, 0, liste_inst, [], buildins, __import__("sys").setrecursionlimit(2**31-1))

print(prog())
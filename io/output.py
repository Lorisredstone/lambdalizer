call = lambda f, *args: f(f, *args[:-1])

liste_inst = [
   ("RESUME", 151, 0, 0, "", 0, 0, False),
   ("LOAD_CONST", 100, 0, 0, "0", 2, 1, False),
   ("STORE_NAME", 90, 0, "i", "i", 4, None, False),
   ("LOAD_NAME", 101, 0, "i", "i", 6, 2, False),
   ("LOAD_CONST", 100, 1, 100000, "100000", 8, None, False),
   ("COMPARE_OP", 107, 0, "<", "<", 10, None, False),
   ("POP_JUMP_FORWARD_IF_FALSE", 114, 36, 90, "to 90", 16, None, False),
   ("PUSH_NULL", 2, None, None, "", 18, 3, True),
   ("LOAD_NAME", 101, 1, "f", "f", 20, None, False),
   ("LOAD_NAME", 101, 0, "i", "i", 22, None, False),
   ("PRECALL", 166, 1, 1, "", 24, None, False),
   ("CALL", 171, 1, 1, "", 28, None, False),
   ("STORE_NAME", 90, 2, "end", "end", 38, None, False),
   ("PUSH_NULL", 2, None, None, "", 40, 4, False),
   ("LOAD_NAME", 101, 3, "print", "print", 42, None, False),
   ("LOAD_NAME", 101, 0, "i", "i", 44, None, False),
   ("LOAD_NAME", 101, 2, "end", "end", 46, None, False),
   ("PRECALL", 166, 2, 2, "", 48, None, False),
   ("CALL", 171, 2, 2, "", 52, None, False),
   ("POP_TOP", 1, None, None, "", 62, None, False),
   ("LOAD_NAME", 101, 0, "i", "i", 64, 5, False),
   ("LOAD_CONST", 100, 2, 1, "1", 66, None, False),
   ("BINARY_OP", 122, 0, 0, "+", 68, None, False),
   ("STORE_NAME", 90, 0, "i", "i", 72, None, False),
   ("LOAD_NAME", 101, 0, "i", "i", 74, 2, False),
   ("LOAD_CONST", 100, 1, 100000, "100000", 76, None, False),
   ("COMPARE_OP", 107, 0, "<", "<", 78, None, False),
   ("POP_JUMP_BACKWARD_IF_TRUE", 176, 34, 18, "to 18", 84, None, False),
   ("LOAD_CONST", 100, 3, None, "None", 86, None, False),
   ("RETURN_VALUE", 83, None, None, "", 88, None, False),
   ("LOAD_CONST", 100, 3, None, "None", 90, None, True),
   ("RETURN_VALUE", 83, None, None, "", 92, None, False)
]

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
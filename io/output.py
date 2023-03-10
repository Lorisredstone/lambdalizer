call = lambda f, *args: f(f, *args[:-1])
liste_inst = [
   (Instruction(opname='RESUME', opcode=151, arg=0, argval=0, argrepr='', offset=0, starts_line=0, is_jump_target=False, positions=Positions(lineno=0, end_lineno=1, col_offset=0, end_col_offset=0)), "RESUME", 151, 0, 0, "", 0, 0, False),
   (Instruction(opname='PUSH_NULL', opcode=2, arg=None, argval=None, argrepr='', offset=2, starts_line=1, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=1)), "PUSH_NULL", 2, None, None, "", 2, 1, False),
   (Instruction(opname='LOAD_NAME', opcode=101, arg=0, argval='f', argrepr='f', offset=4, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=1)), "LOAD_NAME", 101, 0, "f", "f", 4, None, False),
   (Instruction(opname='LOAD_CONST', opcode=100, arg=0, argval=3, argrepr='3', offset=6, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=2, end_col_offset=3)), "LOAD_CONST", 100, 0, 3, "3", 6, None, False),
   (Instruction(opname='LOAD_CONST', opcode=100, arg=1, argval=4, argrepr='4', offset=8, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=5, end_col_offset=6)), "LOAD_CONST", 100, 1, 4, "4", 8, None, False),
   (Instruction(opname='LOAD_CONST', opcode=100, arg=2, argval='b', argrepr="'b'", offset=10, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=10, end_col_offset=13)), "LOAD_CONST", 100, 2, "b", "'b'", 10, None, False),
   (Instruction(opname='LOAD_CONST', opcode=100, arg=3, argval='2', argrepr="'2'", offset=12, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=17, end_col_offset=20)), "LOAD_CONST", 100, 3, "2", "'2'", 12, None, False),
   (Instruction(opname='KW_NAMES', opcode=172, arg=4, argval=<unknown>, argrepr='', offset=14, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=21)), "KW_NAMES", 172, 4, <unknown>, "", 14, None, False),
   (Instruction(opname='PRECALL', opcode=166, arg=4, argval=4, argrepr='', offset=16, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=21)), "PRECALL", 166, 4, 4, "", 16, None, False),
   (Instruction(opname='CALL', opcode=171, arg=4, argval=4, argrepr='', offset=20, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=21)), "CALL", 171, 4, 4, "", 20, None, False),
   (Instruction(opname='RETURN_VALUE', opcode=83, arg=None, argval=None, argrepr='', offset=30, starts_line=None, is_jump_target=False, positions=Positions(lineno=1, end_lineno=1, col_offset=0, end_col_offset=21)), "RETURN_VALUE", 83, None, None, "", 30, None, False)
]


buildins = {
    "print" : print
}

UNKNOWN_INSTRUCTION = lambda  f, cmpt, insts, stack, var_dict : print(f"Error : unknown instruction {insts[cmpt]}")

BINARY_ADD = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__add__(stack.pop(-1))], var_dict]))
BINARY_SUB = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__sub__(stack.pop(-1))], var_dict]))
BINARY_MUL = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__mul__(stack.pop(-1))], var_dict]))
BINARY_DIV = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__truediv__(stack.pop(-1))], var_dict]))
BINARY_POW = (lambda f, cmpt, insts, stack, var_dict : f(*[f, cmpt+1, insts, stack[:-2] + [stack.pop(-2).__pow__(stack.pop(-1))], var_dict]))

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
}.get(insts[cmpt][0], UNKNOWN_INSTRUCTION)(f, cmpt, insts, stack, var_dict)

prog = lambda : call(step, 0, liste_inst, [], buildins, __import__("sys").setrecursionlimit(2**31-1))

print(prog())
import sys
import dis
import os

class File:
    def __init__(self):
        self.lambda_base = open("mod/blank.py", "r").read()
    def setarg(self, nb:int, texte:str) -> None:
        self.lambda_base = self.lambda_base.replace(f"REPLACE_{nb}", texte)
    def tostr(self) -> str:
        return self.lambda_base

class Convertor:
    def __init__(self, input_file:str) -> None:
        self.input_file = input_file
        self.out:File = File()

    def convert(self) -> str:
        bytecode_list = list(dis.Bytecode(open(self.input_file, "r").read()))
        # we make the list of instructions, in tuples
        tuple_list = []
        for inst in bytecode_list:
            if str(inst.opname) == "KW_NAMES":
                tuple_list.append((
                    "\""+str(inst.opname)+"\"",
                    str(inst.opcode),
                    str(inst.arg),
                    "\"UNKNOWN\"",
                    "\""+inst.argrepr+"\"" if isinstance(inst.argrepr, str) else str(inst.argrepr),
                    str(inst.offset),
                    str(inst.starts_line),
                    str(inst.is_jump_target),
                ))
                continue

            tuple_list.append((
                    "\""+str(inst.opname)+"\"",
                    str(inst.opcode),
                    str(inst.arg),
                    "\""+inst.argval+"\"" if isinstance(inst.argval, str) else str(inst.argval),
                    "\""+inst.argrepr+"\"" if isinstance(inst.argrepr, str) else str(inst.argrepr),
                    str(inst.offset),
                    str(inst.starts_line),
                    str(inst.is_jump_target),
                ))
        self.out.setarg(1, "[\n" + ",\n".join([("   (" + ", ".join(thing for thing in element) + ")") for element in tuple_list]) + "\n]")
        return self.out.tostr()
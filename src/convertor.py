import sys
import dis
import os

lambda_base = """lambda fonction, stack, dict, inst_list, inst_pointeur :
...
""".replace("\n", " ")

class Convertor:
    def __init__(self, input_file:str) -> None:
        self.input_file = input_file

    def convert(self) -> str:
        a = list(dis.Bytecode(open(self.input_file, "r").read()))
        for x in a:
            print(x)
        return ""
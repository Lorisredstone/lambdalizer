import sys
import os

import mod.colorprint as colorprint

from src.convertor import Convertor

# si le nombre d'arguments est différent de 3
if len(sys.argv) != 3:
    colorprint.colorprint("Error : wrong number of arguments", color = "red")
    exit(1)

# si le fichier d'entrée n'existe pas
if not os.path.isfile(sys.argv[1]):
    colorprint.colorprint("Error : the input file doesn't exist", color = "red")
    exit(1)

convertor = Convertor(sys.argv[1])
output = convertor.convert()

with open(sys.argv[2], "w") as f:
    f.write(output)
import subprocess
import os

import mod.colorprint as colorprint

import argparse

parser = argparse.ArgumentParser(description='Lance le convertisseur')
parser.add_argument('-i', dest='input', type=str, help='The input file', required=True)
parser.add_argument('-o', dest='output', type=str, help='The output file', required=True)

args = parser.parse_args()

mypy_command = "mypy main.py"
python_command = f"python main.py {args.input} {args.output}"
output_command = f"python {args.output}"

# run mypy with subprocess
p = subprocess.Popen(mypy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
if p.stdout is None:
    colorprint.colorprint("Error : couldnt open a subprocess", color = "red")
    exit(1)
if p.stdout.read() == b'Success: no issues found in 1 source file\r\n':
    colorprint.colorprint("Mypy passed for the whole project !", color = "green")
    os.system(python_command)
    colorprint.colorprint("Python passed for the whole project !", color = "green")
    colorprint.colorprint("Launching the output program...", color = "green")
    p_process = subprocess.Popen(output_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p_process.stdout is None or p_process.stderr is None:
        colorprint.colorprint("Error : couldnt open a subprocess", color = "red")
        exit(1)
    if p_process.stdout.read() != b'':
        colorprint.colorprint(f"Stdout : {p_process.stdout.read()}", color = "green")
    if p_process.stderr.read() != b'':
        colorprint.colorprint(f"Stderr : {p_process.stderr.read()}", color = "red")
else:
    print("Mypy failed !")
    colorprint.colorprint("Mypy failed for the whole project !", color = "red")
    os.system(mypy_command)
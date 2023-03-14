f = lambda x : str((lambda f, *args: f(f, *args[:-1]))(lambda f, nb, total : f(f, nb-1, total * nb) if nb != 1 else total, x, 1, __import__("sys").setrecursionlimit(2**31-1))).strip("0")[-4:]

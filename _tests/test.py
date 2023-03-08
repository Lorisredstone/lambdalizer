call = lambda f, *args: f(f, *args[:-1]) if args[0] else 0
inter = lambda f, stop_c, inst_p, inst_list, var_dict, stack:...
somme = lambda f, stop_c, k, total : f(f, k > 1, k-1, total+k) if stop_c else total
somme_tot = lambda x : call(somme, 1, x, 0, __import__("sys").setrecursionlimit(2**31-1))
print(somme_tot(int(input())))
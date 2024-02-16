x = 10
stm1 = "x**2 + 4*x + 4"
stm2 = "x + 4 * 5"
print(locals())
result = eval(stm2, globals(), locals())
print(result)
print(locals())
print(globals())

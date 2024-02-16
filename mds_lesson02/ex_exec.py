exec('''print("hello world")
x = 10
print(x)''')

x = 100
stm = """
rr = x + 4 * 5
print(rr)
"""


def baz():
    x = 10
    print(locals())
    exec(stm, globals(), locals())
    print(locals())
    print(globals())
    print(locals()["rr"])


baz()

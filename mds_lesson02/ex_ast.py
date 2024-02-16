import ast

# with open('main.py', encoding='utf-8') as f:
#     tree = ast.parse(f.read())
#     exec(compile(tree, 'main.py', 'exec'))

code = "print('hello world')"

tree = ast.parse(code)
r = ast.dump(tree, annotate_fields=False)
print(r)

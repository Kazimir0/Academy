import ast
from collections import defaultdict

filename = "app.py"

with open(filename, "r", encoding="utf-8") as file:
    source = file.read()

tree = ast.parse(source)

ids = defaultdict(set)

for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "callback":
        decorator = node
        if node.args:
            for output in node.args[0:1]:  # Outputs
                if isinstance(output, ast.List):
                    for out in output.elts:
                        if isinstance(out, ast.Call):
                            for kw in out.keywords:
                                if kw.arg == 'component_id':
                                    ids["Output"].add(eval(compile(ast.Expression(kw.value), filename, "eval")))
                elif isinstance(output, ast.Call):
                    for kw in output.keywords:
                        if kw.arg == 'component_id':
                            ids["Output"].add(eval(compile(ast.Expression(kw.value), filename, "eval")))

        for keyword in node.keywords:
            if keyword.arg == "inputs" or keyword.arg == "Input":
                if isinstance(keyword.value, ast.List):
                    for inp in keyword.value.elts:
                        for kw in inp.keywords:
                            if kw.arg == "component_id":
                                ids["Input"].add(eval(compile(ast.Expression(kw.value), filename, "eval")))
            elif keyword.arg == "state" or keyword.arg == "State":
                if isinstance(keyword.value, ast.List):
                    for st in keyword.value.elts:
                        for kw in st.keywords:
                            if kw.arg == "component_id":
                                ids["State"].add(eval(compile(ast.Expression(kw.value), filename, "eval")))

# Extra: extrage și din `Input(...)` sau `Output(...)` din `@app.callback` cu poziționali
class ComponentIDExtractor(ast.NodeVisitor):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ["Input", "Output", "State"]:
            if node.args and isinstance(node.args[0], ast.Constant):
                ids[node.func.id].add(node.args[0].value)
        self.generic_visit(node)

extractor = ComponentIDExtractor()
extractor.visit(tree)

# Afișează lista finală
print("\n Lista unica de ID-uri folosite în callback-uri:\n")
for category in ["Input", "Output", "State"]:
    print(f"🔹 {category}:")
    for component_id in sorted(ids[category]):
        print(f"  - {component_id}")
    print()

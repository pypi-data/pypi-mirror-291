import ast
def sparta_bcfa9a292a(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_edbaf7d245(script_text):return sparta_bcfa9a292a(script_text)
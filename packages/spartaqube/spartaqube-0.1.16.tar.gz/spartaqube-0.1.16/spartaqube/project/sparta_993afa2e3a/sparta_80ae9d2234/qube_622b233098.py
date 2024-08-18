import ast
def sparta_9d848e2f95(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_28c091cbaa(script_text):return sparta_9d848e2f95(script_text)
import ast
def sparta_83f93c2924(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_9714693870(script_text):return sparta_83f93c2924(script_text)
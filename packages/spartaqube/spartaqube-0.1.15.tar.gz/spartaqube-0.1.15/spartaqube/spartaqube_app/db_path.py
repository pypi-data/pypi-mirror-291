_A='windows'
import os,sys,getpass,platform
def sparta_4651270f37(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_bdd41e1710():
	A=platform.system()
	if A=='Windows':return _A
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
def sparta_55d87ca87c():
	B=sparta_bdd41e1710()
	if B==_A:A=f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\SpartaQube\\data"
	elif B=='linux':A=os.path.expanduser('~/SpartaQube/data')
	elif B=='mac':A=os.path.expanduser('~/Library/Application Support\\SpartaQube\\data')
	sparta_4651270f37(A);C=os.path.join(A,'db.sqlite3');return C
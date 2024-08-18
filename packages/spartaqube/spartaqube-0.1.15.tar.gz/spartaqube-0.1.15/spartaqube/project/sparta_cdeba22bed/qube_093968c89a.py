import time
def sparta_d93644b567():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_d93644b567()
def sparta_161b35a7cc(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_1e53dbf8e7():sparta_161b35a7cc(False)
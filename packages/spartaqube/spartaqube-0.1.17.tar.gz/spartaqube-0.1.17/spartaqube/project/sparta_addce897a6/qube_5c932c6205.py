import time
def sparta_f0e37778a8():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_f0e37778a8()
def sparta_b26ee1c16a(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_2dec14e0f3():sparta_b26ee1c16a(False)
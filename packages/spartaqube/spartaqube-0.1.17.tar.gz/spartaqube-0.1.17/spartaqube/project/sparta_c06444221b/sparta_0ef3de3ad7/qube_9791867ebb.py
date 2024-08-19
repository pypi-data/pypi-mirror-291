_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_866369bc29.sparta_a6cd567dfa import qube_bc116ca566 as qube_bc116ca566
from project.sparta_addce897a6.sparta_cca83b7c2a.qube_bb2a0cc88d import sparta_51c79229a7
@csrf_exempt
def sparta_325e7683c6(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_bc116ca566.sparta_325e7683c6(B)
@csrf_exempt
def sparta_fdfddf2339(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_6ef8ece57f(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_7f5f5c7acf(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)
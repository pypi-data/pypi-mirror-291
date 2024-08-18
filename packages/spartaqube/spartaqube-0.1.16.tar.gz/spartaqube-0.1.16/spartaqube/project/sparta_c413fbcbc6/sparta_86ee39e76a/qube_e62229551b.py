_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_993afa2e3a.sparta_db74d25518 import qube_1bfe878a6d as qube_1bfe878a6d
from project.sparta_06ab2796ce.sparta_6d86447bae.qube_ff414021cf import sparta_6d45c7ccfc
@csrf_exempt
def sparta_23ee2404c9(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_1bfe878a6d.sparta_23ee2404c9(B)
@csrf_exempt
def sparta_3739d862ff(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_c8aa3e6655(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_dd8efe19fa(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)
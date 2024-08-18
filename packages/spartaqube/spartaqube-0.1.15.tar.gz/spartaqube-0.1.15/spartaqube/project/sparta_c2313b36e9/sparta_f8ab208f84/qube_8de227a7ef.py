_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_d9c09478c6.sparta_6eb4e27988 import qube_cde4203e48 as qube_cde4203e48
from project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d import sparta_60c6b775bf
@csrf_exempt
def sparta_4725fd660b(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_cde4203e48.sparta_4725fd660b(B)
@csrf_exempt
def sparta_59cc14f2a0(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_7b5f687479(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_7968bace18(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)
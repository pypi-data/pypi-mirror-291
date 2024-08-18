_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_993afa2e3a.sparta_a891059c55 import qube_ccc96ea90b as qube_ccc96ea90b
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_4a0bc2deed
@csrf_exempt
@sparta_4a0bc2deed
def sparta_74fb067566(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.sparta_74fb067566(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_6380d04987(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_ccc96ea90b.sparta_6380d04987(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_9d2bdde42b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_ccc96ea90b.sparta_9d2bdde42b(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_f4b3de615e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.sparta_f4b3de615e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_0f5f347811(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.sparta_0f5f347811(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_f1c0b4c148(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.sparta_f1c0b4c148(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_5ab19fc22c(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_ccc96ea90b.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_b6b2138cc0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_f60a587b6e(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_ccc96ea90b.sparta_f60a587b6e(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_416c864241(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_ccc96ea90b.sparta_416c864241(A,C);E=json.dumps(D);return HttpResponse(E)
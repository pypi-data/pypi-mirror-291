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
from project.sparta_866369bc29.sparta_2f607bca8c import qube_c85802a4f7 as qube_c85802a4f7
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_8c884aad0b
@csrf_exempt
@sparta_8c884aad0b
def sparta_86be17f644(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.sparta_86be17f644(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_6160ce69a7(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_c85802a4f7.sparta_6160ce69a7(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_8c884aad0b
def sparta_037d26bd66(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_c85802a4f7.sparta_037d26bd66(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_8c884aad0b
def sparta_3674dcf3e4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.sparta_3674dcf3e4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_02b2b5f537(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.sparta_02b2b5f537(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_f43d950765(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.sparta_f43d950765(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_618801cc85(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_c85802a4f7.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_8c884aad0b
def sparta_83f62f5c9c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_cc3a4e0034(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_c85802a4f7.sparta_cc3a4e0034(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_6d068456dc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c85802a4f7.sparta_6d068456dc(A,C);E=json.dumps(D);return HttpResponse(E)
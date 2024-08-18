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
from project.sparta_d9c09478c6.sparta_1d3affc1d1 import qube_6b84b69e1b as qube_6b84b69e1b
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_a937a5f24c
@csrf_exempt
@sparta_a937a5f24c
def sparta_1b85c2733c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.sparta_1b85c2733c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_950b84d70a(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_6b84b69e1b.sparta_950b84d70a(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_a937a5f24c
def sparta_ff67c82dc1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_6b84b69e1b.sparta_ff67c82dc1(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_a937a5f24c
def sparta_6e01ceba7d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.sparta_6e01ceba7d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_bb3fa38a91(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.sparta_bb3fa38a91(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_d48337e863(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.sparta_d48337e863(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_b636ccac7b(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_6b84b69e1b.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_a937a5f24c
def sparta_2fb414b856(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_b1d9c860ca(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_6b84b69e1b.sparta_b1d9c860ca(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_a74b1a5412(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6b84b69e1b.sparta_a74b1a5412(A,C);E=json.dumps(D);return HttpResponse(E)
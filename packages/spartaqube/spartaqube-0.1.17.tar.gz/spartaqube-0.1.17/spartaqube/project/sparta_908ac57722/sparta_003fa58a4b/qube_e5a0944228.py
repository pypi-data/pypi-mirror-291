_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='login'
_J='POST'
_I=False
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_addce897a6.sparta_cca83b7c2a.qube_bb2a0cc88d as qube_bb2a0cc88d
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_9eee2d8f98
from project.sparta_866369bc29.sparta_a6cd567dfa import qube_bc116ca566 as qube_bc116ca566
from project.sparta_c06444221b.sparta_0ef3de3ad7 import qube_9791867ebb as qube_9791867ebb
from project.models import LoginLocation,UserProfile
def sparta_a7990166d2():return{'bHasCompanyEE':-1}
def sparta_3941598eca(request):B=request;A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_9eee2d8f98
def sparta_0681eb126a(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_ac1b2649d3(C,A)
def sparta_22eb064122(request,redirectUrl):return sparta_ac1b2649d3(request,redirectUrl)
def sparta_ac1b2649d3(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_bc116ca566.sparta_cf6acb7a03(F):return sparta_3941598eca(A)
				login(A,F);K,L=qube_bb2a0cc88d.sparta_0695838d08();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);B.update(qube_bb2a0cc88d.sparta_9a1f514272(A));B[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_a7990166d2());return render(A,'dist/project/auth/login.html',B)
@sparta_9eee2d8f98
def sparta_f1a7916dcd(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_bc116ca566.sparta_c53640b219()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_bc116ca566.sparta_8b8bc4a228(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_bc116ca566.sparta_325e7683c6(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);C.update(qube_bb2a0cc88d.sparta_9a1f514272(A));C[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_a7990166d2());return render(A,'dist/project/auth/registration.html',C)
def sparta_d08f670212(request):A=request;B=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);B[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_eaa9e00762(request,token):
	A=request;B=qube_bc116ca566.sparta_375345e40c(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);D[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();return redirect(_K)
def sparta_ad37f147f6(request):logout(request);return redirect(_K)
def sparta_47b096b474(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_74b705285b(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_bc116ca566.sparta_74b705285b(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);C.update(qube_bb2a0cc88d.sparta_9a1f514272(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);D.update(qube_bb2a0cc88d.sparta_9a1f514272(A));D[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_a7990166d2());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_14b2d51ef4(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_bc116ca566.sparta_14b2d51ef4(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_bb2a0cc88d.sparta_a8bb6e74e5(D);A.update(qube_bb2a0cc88d.sparta_9a1f514272(D));A[_C]=qube_bb2a0cc88d.sparta_da71b00c6d();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_a7990166d2());return render(D,_N,A)
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
import project.sparta_06ab2796ce.sparta_6d86447bae.qube_ff414021cf as qube_ff414021cf
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_8ffab28e13
from project.sparta_993afa2e3a.sparta_db74d25518 import qube_1bfe878a6d as qube_1bfe878a6d
from project.sparta_c413fbcbc6.sparta_86ee39e76a import qube_e62229551b as qube_e62229551b
from project.models import LoginLocation,UserProfile
def sparta_6137a9ff27():return{'bHasCompanyEE':-1}
def sparta_a94bb97479(request):B=request;A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=qube_ff414021cf.sparta_d36d3ea634();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_8ffab28e13
def sparta_0fe3de33cd(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_f18441106d(C,A)
def sparta_76ee268459(request,redirectUrl):return sparta_f18441106d(request,redirectUrl)
def sparta_f18441106d(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_1bfe878a6d.sparta_eacb946e48(F):return sparta_a94bb97479(A)
				login(A,F);K,L=qube_ff414021cf.sparta_3ca25e3ce7();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_ff414021cf.sparta_bce5bb4727(A);B.update(qube_ff414021cf.sparta_87914c7112(A));B[_C]=qube_ff414021cf.sparta_d36d3ea634();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_6137a9ff27());return render(A,'dist/project/auth/login.html',B)
@sparta_8ffab28e13
def sparta_af2efbc887(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_1bfe878a6d.sparta_f2a22f0b94()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_1bfe878a6d.sparta_4bf278711d(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_1bfe878a6d.sparta_23ee2404c9(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_ff414021cf.sparta_bce5bb4727(A);C.update(qube_ff414021cf.sparta_87914c7112(A));C[_C]=qube_ff414021cf.sparta_d36d3ea634();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_6137a9ff27());return render(A,'dist/project/auth/registration.html',C)
def sparta_b589d51171(request):A=request;B=qube_ff414021cf.sparta_bce5bb4727(A);B[_C]=qube_ff414021cf.sparta_d36d3ea634();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_c897aa4cec(request,token):
	A=request;B=qube_1bfe878a6d.sparta_23831809c0(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_ff414021cf.sparta_bce5bb4727(A);D[_C]=qube_ff414021cf.sparta_d36d3ea634();return redirect(_K)
def sparta_ebddae4589(request):logout(request);return redirect(_K)
def sparta_104031ff9d(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_91b20675fe(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_1bfe878a6d.sparta_91b20675fe(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_ff414021cf.sparta_bce5bb4727(A);C.update(qube_ff414021cf.sparta_87914c7112(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_ff414021cf.sparta_d36d3ea634();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_ff414021cf.sparta_bce5bb4727(A);D.update(qube_ff414021cf.sparta_87914c7112(A));D[_C]=qube_ff414021cf.sparta_d36d3ea634();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_6137a9ff27());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_d5bd0c8708(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_1bfe878a6d.sparta_d5bd0c8708(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_ff414021cf.sparta_bce5bb4727(D);A.update(qube_ff414021cf.sparta_87914c7112(D));A[_C]=qube_ff414021cf.sparta_d36d3ea634();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_6137a9ff27());return render(D,_N,A)
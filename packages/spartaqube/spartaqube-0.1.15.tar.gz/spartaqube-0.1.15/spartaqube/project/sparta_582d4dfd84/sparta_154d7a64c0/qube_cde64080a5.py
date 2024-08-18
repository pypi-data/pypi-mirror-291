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
import project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d as qube_0d08addb0d
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_8eb9b85134
from project.sparta_d9c09478c6.sparta_6eb4e27988 import qube_cde4203e48 as qube_cde4203e48
from project.sparta_c2313b36e9.sparta_f8ab208f84 import qube_8de227a7ef as qube_8de227a7ef
from project.models import LoginLocation,UserProfile
def sparta_24c5fccf09():return{'bHasCompanyEE':-1}
def sparta_dd95f302cf(request):B=request;A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=qube_0d08addb0d.sparta_19b6063cc7();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_8eb9b85134
def sparta_38fb67a5f2(request):
	C=request;B='/';A=C.GET.get(_K)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_db29b56fd4(C,A)
def sparta_ede5fc3e3e(request,redirectUrl):return sparta_db29b56fd4(request,redirectUrl)
def sparta_db29b56fd4(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_I;H='Email or password incorrect'
	if A.method==_J:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_cde4203e48.sparta_ab024ea397(F):return sparta_dd95f302cf(A)
				login(A,F);K,L=qube_0d08addb0d.sparta_e187331a72();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_0d08addb0d.sparta_cdb85dde13(A);B.update(qube_0d08addb0d.sparta_65e4d49ca8(A));B[_C]=qube_0d08addb0d.sparta_19b6063cc7();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_24c5fccf09());return render(A,'dist/project/auth/login.html',B)
@sparta_8eb9b85134
def sparta_66326ed2de(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_I;F=qube_cde4203e48.sparta_d44f2c6719()
	if A.method==_J:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_cde4203e48.sparta_5e78a434ca(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_cde4203e48.sparta_4725fd660b(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_0d08addb0d.sparta_cdb85dde13(A);C.update(qube_0d08addb0d.sparta_65e4d49ca8(A));C[_C]=qube_0d08addb0d.sparta_19b6063cc7();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_24c5fccf09());return render(A,'dist/project/auth/registration.html',C)
def sparta_9a7643373a(request):A=request;B=qube_0d08addb0d.sparta_cdb85dde13(A);B[_C]=qube_0d08addb0d.sparta_19b6063cc7();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_b9d5630552(request,token):
	A=request;B=qube_cde4203e48.sparta_ede5a927c9(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_0d08addb0d.sparta_cdb85dde13(A);D[_C]=qube_0d08addb0d.sparta_19b6063cc7();return redirect(_K)
def sparta_2dbe5ab0ce(request):logout(request);return redirect(_K)
def sparta_0db1c9107d(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_78cad2043d(request):
	A=request;E='';F=_I
	if A.method==_J:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_cde4203e48.sparta_78cad2043d(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_0d08addb0d.sparta_cdb85dde13(A);C.update(qube_0d08addb0d.sparta_65e4d49ca8(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_0d08addb0d.sparta_19b6063cc7();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_0d08addb0d.sparta_cdb85dde13(A);D.update(qube_0d08addb0d.sparta_65e4d49ca8(A));D[_C]=qube_0d08addb0d.sparta_19b6063cc7();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_24c5fccf09());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_f0a4a2b1f0(request):
	D=request;E='';B=_I
	if D.method==_J:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_cde4203e48.sparta_f0a4a2b1f0(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_0d08addb0d.sparta_cdb85dde13(D);A.update(qube_0d08addb0d.sparta_65e4d49ca8(D));A[_C]=qube_0d08addb0d.sparta_19b6063cc7();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_24c5fccf09());return render(D,_N,A)
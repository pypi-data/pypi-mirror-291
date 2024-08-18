from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_06ab2796ce.sparta_6d86447bae.qube_ff414021cf as qube_ff414021cf
from project.models import UserProfile
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_8ffab28e13
from project.sparta_b59b8fcd05.sparta_6953b3c627.qube_4a0cd9e43b import sparta_6137a9ff27
@sparta_8ffab28e13
@login_required(redirect_field_name='login')
def sparta_3e3c17855d(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_ff414021cf.sparta_bce5bb4727(B);A.update(qube_ff414021cf.sparta_e8312e6c3f(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_6137a9ff27());return render(B,'dist/project/auth/settings.html',A)
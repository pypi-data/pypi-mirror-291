from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d as qube_0d08addb0d
from project.models import UserProfile
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_8eb9b85134
from project.sparta_582d4dfd84.sparta_154d7a64c0.qube_cde64080a5 import sparta_24c5fccf09
@sparta_8eb9b85134
@login_required(redirect_field_name='login')
def sparta_9fb8d561e4(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_0d08addb0d.sparta_cdb85dde13(B);A.update(qube_0d08addb0d.sparta_49252b01bd(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_24c5fccf09());return render(B,'dist/project/auth/settings.html',A)
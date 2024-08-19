from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_addce897a6.sparta_cca83b7c2a.qube_bb2a0cc88d as qube_bb2a0cc88d
from project.models import UserProfile
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_9eee2d8f98
from project.sparta_908ac57722.sparta_003fa58a4b.qube_e5a0944228 import sparta_a7990166d2
@sparta_9eee2d8f98
@login_required(redirect_field_name='login')
def sparta_9f49e7d0cb(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A.update(qube_bb2a0cc88d.sparta_7e43fffad4(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_a7990166d2());return render(B,'dist/project/auth/settings.html',A)
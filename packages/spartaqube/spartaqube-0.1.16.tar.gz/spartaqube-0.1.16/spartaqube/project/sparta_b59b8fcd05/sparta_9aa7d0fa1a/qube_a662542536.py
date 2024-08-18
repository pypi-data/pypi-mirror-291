from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_8ffab28e13
from project.sparta_993afa2e3a.sparta_34ab35b352 import qube_670b7ef163 as qube_670b7ef163
from project.models import UserProfile
import project.sparta_06ab2796ce.sparta_6d86447bae.qube_ff414021cf as qube_ff414021cf
@sparta_8ffab28e13
@login_required(redirect_field_name='login')
def sparta_59385528d4(request):
	E='avatarImg';B=request;A=qube_ff414021cf.sparta_bce5bb4727(B);A['menuBar']=-1;F=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_8ffab28e13
@login_required(redirect_field_name='login')
def sparta_6cc3e23ea4(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_59385528d4(A)
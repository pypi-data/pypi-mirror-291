from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_8eb9b85134
from project.sparta_d9c09478c6.sparta_9f1b5b635c import qube_d295f7b9d0 as qube_d295f7b9d0
from project.models import UserProfile
import project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d as qube_0d08addb0d
@sparta_8eb9b85134
@login_required(redirect_field_name='login')
def sparta_1d7bc516b7(request):
	E='avatarImg';B=request;A=qube_0d08addb0d.sparta_cdb85dde13(B);A['menuBar']=-1;F=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_8eb9b85134
@login_required(redirect_field_name='login')
def sparta_5738fd34a5(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_1d7bc516b7(A)
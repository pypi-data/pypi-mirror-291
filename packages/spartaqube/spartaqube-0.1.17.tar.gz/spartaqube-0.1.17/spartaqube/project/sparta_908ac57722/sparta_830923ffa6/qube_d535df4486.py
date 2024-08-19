from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_9eee2d8f98
from project.sparta_866369bc29.sparta_9a70c866a7 import qube_c94008b0ab as qube_c94008b0ab
from project.models import UserProfile
import project.sparta_addce897a6.sparta_cca83b7c2a.qube_bb2a0cc88d as qube_bb2a0cc88d
@sparta_9eee2d8f98
@login_required(redirect_field_name='login')
def sparta_0dfbd8a8fb(request):
	E='avatarImg';B=request;A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A['menuBar']=-1;F=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_9eee2d8f98
@login_required(redirect_field_name='login')
def sparta_fbf4e13773(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_0dfbd8a8fb(A)
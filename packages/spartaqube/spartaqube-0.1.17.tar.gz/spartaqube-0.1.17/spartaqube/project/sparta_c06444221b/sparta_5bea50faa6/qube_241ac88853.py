_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_866369bc29.sparta_f3380873e7 import qube_08bf8b4a4a as qube_08bf8b4a4a
from project.sparta_866369bc29.sparta_9a70c866a7 import qube_c94008b0ab as qube_c94008b0ab
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_8c884aad0b
@csrf_exempt
@sparta_8c884aad0b
def sparta_1283cefc6f(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_c94008b0ab.sparta_43348df6a7(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_08bf8b4a4a.sparta_1283cefc6f(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_8c884aad0b
def sparta_cd967a9d53(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_08bf8b4a4a.sparta_77eacfc34e(C,A.user);E=json.dumps(D);return HttpResponse(E)
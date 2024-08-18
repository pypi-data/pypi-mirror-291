_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_d9c09478c6.sparta_64544077ec import qube_653ae7ff6d as qube_653ae7ff6d
from project.sparta_d9c09478c6.sparta_9f1b5b635c import qube_d295f7b9d0 as qube_d295f7b9d0
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_a937a5f24c
@csrf_exempt
@sparta_a937a5f24c
def sparta_cec50689f4(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_d295f7b9d0.sparta_d02bdca957(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_653ae7ff6d.sparta_cec50689f4(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_a937a5f24c
def sparta_001b3db896(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_653ae7ff6d.sparta_39e5a42454(C,A.user);E=json.dumps(D);return HttpResponse(E)
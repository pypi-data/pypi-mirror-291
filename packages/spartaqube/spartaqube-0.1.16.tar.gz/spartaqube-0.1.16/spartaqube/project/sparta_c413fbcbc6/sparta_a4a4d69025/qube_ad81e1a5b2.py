_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_993afa2e3a.sparta_b322c0aff5 import qube_bbbe8ccfda as qube_bbbe8ccfda
from project.sparta_993afa2e3a.sparta_34ab35b352 import qube_670b7ef163 as qube_670b7ef163
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_4a0bc2deed
@csrf_exempt
@sparta_4a0bc2deed
def sparta_327cfac579(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_670b7ef163.sparta_c473a91fad(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_bbbe8ccfda.sparta_327cfac579(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_7091a0e3a9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_bbbe8ccfda.sparta_2c17e630cf(C,A.user);E=json.dumps(D);return HttpResponse(E)
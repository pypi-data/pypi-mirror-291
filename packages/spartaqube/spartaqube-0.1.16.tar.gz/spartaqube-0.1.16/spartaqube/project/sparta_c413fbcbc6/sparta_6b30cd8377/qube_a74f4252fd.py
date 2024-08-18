import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_993afa2e3a.sparta_c59d65466e import qube_6761bf71c7 as qube_6761bf71c7
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_4a0bc2deed
@csrf_exempt
@sparta_4a0bc2deed
def sparta_dc88811e01(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_6761bf71c7.sparta_dc88811e01(B,A.user);I=json.dumps(H);return HttpResponse(I)
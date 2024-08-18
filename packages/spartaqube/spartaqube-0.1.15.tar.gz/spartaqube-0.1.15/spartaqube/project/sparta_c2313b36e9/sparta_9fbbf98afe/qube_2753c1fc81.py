import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_d9c09478c6.sparta_567ed7476a import qube_0b64a68279 as qube_0b64a68279
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_a937a5f24c
@csrf_exempt
@sparta_a937a5f24c
def sparta_282393e34a(request):G='api_func';F='key';E='utf-8';A=request;C=A.body.decode(E);C=A.POST.get(F);D=A.body.decode(E);D=A.POST.get(G);B=dict();B[F]=C;B[G]=D;H=qube_0b64a68279.sparta_282393e34a(B,A.user);I=json.dumps(H);return HttpResponse(I)
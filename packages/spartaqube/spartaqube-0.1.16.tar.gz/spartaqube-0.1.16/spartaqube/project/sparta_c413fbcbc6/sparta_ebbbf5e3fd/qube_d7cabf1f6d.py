_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='Content-Disposition'
_C='res'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_993afa2e3a.sparta_1ca59f1cdc import qube_13b754891b as qube_13b754891b
from project.sparta_993afa2e3a.sparta_1ca59f1cdc import qube_3ebbcc697e as qube_3ebbcc697e
from project.sparta_993afa2e3a.sparta_28f2f63dd2 import qube_581ca2ff5f as qube_581ca2ff5f
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_4a0bc2deed
@csrf_exempt
@sparta_4a0bc2deed
def sparta_e939da26d7(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_13b754891b.sparta_d28d3e34db(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_e733fe4060(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_751a9141f6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_421f0ac661(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_428f99b455(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_4f73b7777c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_04ed69b48e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_8f2fcbedb4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_3ebbcc697e.sparta_d2d8c1906d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_81f30fd557(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_9f026886d0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_3f8c8750fd(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_d9be971537(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_5bf051fa99(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_fe78c87dd2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_4aec9c54ac(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_13b754891b.sparta_8e0c818874(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_4a0bc2deed
def sparta_6dbaeb78c2(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_13b754891b.sparta_461564f350(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_4a0bc2deed
def sparta_183f7f691d(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_13b754891b.sparta_e7ab3e8d15(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_4a0bc2deed
def sparta_12ee16f4d5(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_13b754891b.sparta_4933be8c9a(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A
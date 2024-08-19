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
from project.sparta_866369bc29.sparta_ac5ad4c04d import qube_31554659a1 as qube_31554659a1
from project.sparta_866369bc29.sparta_ac5ad4c04d import qube_8715ed393a as qube_8715ed393a
from project.sparta_866369bc29.sparta_e84ec90a6d import qube_e916c5d1d8 as qube_e916c5d1d8
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_8c884aad0b
@csrf_exempt
@sparta_8c884aad0b
def sparta_dfd394baab(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_31554659a1.sparta_7864523e78(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_8c884aad0b
def sparta_bdedad4d33(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_89d2d9b6d2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_4862dc44f6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_de82ececc6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_dbaeecd43c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_f4930e5af6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_cb5fbe4d5b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_8715ed393a.sparta_7c3e409233(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_8798b51cf2(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_17439e2bce(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_213388dac8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_862d432060(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_4fc3f30730(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_4a6357ee1c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_ace84aa77e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_31554659a1.sparta_b7521164b8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_8c884aad0b
def sparta_8ddf5c36c7(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_31554659a1.sparta_6b238e0c89(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_8c884aad0b
def sparta_22aaaa82b5(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_31554659a1.sparta_20631d492c(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_8c884aad0b
def sparta_a3db873a49(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_31554659a1.sparta_de80ed9fb3(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A
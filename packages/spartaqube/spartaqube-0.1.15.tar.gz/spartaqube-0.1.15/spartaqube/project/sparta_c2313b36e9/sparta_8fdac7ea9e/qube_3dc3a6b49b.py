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
from project.sparta_d9c09478c6.sparta_7ba049b6aa import qube_a16f24287c as qube_a16f24287c
from project.sparta_d9c09478c6.sparta_7ba049b6aa import qube_e8fdbcab26 as qube_e8fdbcab26
from project.sparta_d9c09478c6.sparta_b184892b51 import qube_8a75fefeff as qube_8a75fefeff
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_a937a5f24c
@csrf_exempt
@sparta_a937a5f24c
def sparta_1b58dc60d4(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_a16f24287c.sparta_f469db892a(E,A.user,B[D])
	else:C={_C:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_a937a5f24c
def sparta_a4d0db6e75(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_f1e98e51cf(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_88b2086886(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_e8b08d8158(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_dcba4a6d48(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_56fb05fa01(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_22e6bcd68d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_e8fdbcab26.sparta_0ef5cb51b2(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_a6829313ee(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_caab3d1049(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_5f2beeca95(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_c6b268829a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_e415a1d0e8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_1407f22b87(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_cb9f5c5e2f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_a16f24287c.sparta_901f626407(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_a937a5f24c
def sparta_3d62fecae2(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_a16f24287c.sparta_85cbd62dbe(J,A.user)
	if C[_C]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_D]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_a937a5f24c
def sparta_4a5c681cbb(request):
	E='folderName';C=request;F=C.GET[_B];D=C.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};B=qube_a16f24287c.sparta_68ca4a75d9(G,C.user);print(_C);print(B)
	if B[_C]==1:H=B['zip'];I=B[_H];A=HttpResponse();A.write(H.getvalue());A[_D]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_D]=_F.format(K)
	return A
@csrf_exempt
@sparta_a937a5f24c
def sparta_ba8b1cc68c(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_a16f24287c.sparta_0a557e5b21(F,B.user)
	if C[_C]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_D]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_D]=_F.format(J)
	return A
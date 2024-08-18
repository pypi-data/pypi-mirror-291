_K='has_access'
_J='session'
_I='plot_name'
_H='plot_chart_id'
_G=False
_F='login'
_E='plot_db_chart_obj'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d as qube_0d08addb0d
from project.sparta_d9c09478c6.sparta_6eb4e27988.qube_cde4203e48 import sparta_8eb9b85134
from project.sparta_d9c09478c6.sparta_0849603d77 import qube_ba9501194a as qube_ba9501194a
@csrf_exempt
@sparta_8eb9b85134
@login_required(redirect_field_name=_F)
def sparta_5e0f48475b(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=7;D=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_8eb9b85134
@login_required(redirect_field_name=_F)
def sparta_28b2ac57af(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_ba9501194a.sparta_37ba1e4b88(C,A.user);D=not E[_K]
	if D:return sparta_5e0f48475b(A)
	B=qube_0d08addb0d.sparta_cdb85dde13(A);B[_C]=7;F=qube_0d08addb0d.sparta_49252b01bd(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_8eb9b85134
def sparta_321549a060(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_fe7bfba08b(A,B)
@csrf_exempt
@sparta_8eb9b85134
def sparta_5bb1dbe201(request,widget_id,session_id,api_token_id):return sparta_fe7bfba08b(request,widget_id,session_id)
def sparta_fe7bfba08b(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_ba9501194a.sparta_2db519688a(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_5e0f48475b(B)
	A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=7;I=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_8eb9b85134
def sparta_088b06d750(request,session_id,api_token_id):B=request;A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=7;C=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_8eb9b85134
@login_required(redirect_field_name=_F)
def sparta_37800b0a7d(request):
	J=',\n    ';B=request;C=B.GET.get('id');E=_G
	if C is _B:E=_A
	else:F=qube_ba9501194a.sparta_37ba1e4b88(C,B.user);E=not F[_K]
	if E:return sparta_5e0f48475b(B)
	K=qube_ba9501194a.sparta_a6f98aaee1(F[_E]);D='';G=0
	for(H,I)in K.items():
		if G>0:D+=J
		if I==1:D+=f"{H}=input_1"
		else:L=str(J.join([f"input_{A}"for A in range(I)]));D+=f"{H}=[{L}]"
		G+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_data(\n    "{C}",\n    {D}\n)';A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=7;O=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=F[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_8eb9b85134
def sparta_b8e9946e69(request,session_id,api_token_id,json_vars_html):B=request;A=qube_0d08addb0d.sparta_cdb85dde13(B);A[_C]=7;C=qube_0d08addb0d.sparta_49252b01bd(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)
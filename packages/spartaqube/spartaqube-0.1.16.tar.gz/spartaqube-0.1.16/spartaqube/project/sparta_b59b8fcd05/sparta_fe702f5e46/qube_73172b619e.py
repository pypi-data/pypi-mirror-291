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
import project.sparta_06ab2796ce.sparta_6d86447bae.qube_ff414021cf as qube_ff414021cf
from project.sparta_993afa2e3a.sparta_db74d25518.qube_1bfe878a6d import sparta_8ffab28e13
from project.sparta_993afa2e3a.sparta_44f1e7eacf import qube_cf975e3d38 as qube_cf975e3d38
@csrf_exempt
@sparta_8ffab28e13
@login_required(redirect_field_name=_F)
def sparta_6e5e202fc5(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=7;D=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_8ffab28e13
@login_required(redirect_field_name=_F)
def sparta_57f19cb9c7(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_cf975e3d38.sparta_c0fb6e4d66(C,A.user);D=not E[_K]
	if D:return sparta_6e5e202fc5(A)
	B=qube_ff414021cf.sparta_bce5bb4727(A);B[_C]=7;F=qube_ff414021cf.sparta_e8312e6c3f(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_8ffab28e13
def sparta_b51dcde340(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_cecbc809d3(A,B)
@csrf_exempt
@sparta_8ffab28e13
def sparta_2bb48cf51c(request,widget_id,session_id,api_token_id):return sparta_cecbc809d3(request,widget_id,session_id)
def sparta_cecbc809d3(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_cf975e3d38.sparta_41e36e4ab4(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_6e5e202fc5(B)
	A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=7;I=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_8ffab28e13
def sparta_f5ef642a44(request,session_id,api_token_id):B=request;A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=7;C=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_8ffab28e13
@login_required(redirect_field_name=_F)
def sparta_ebe10e4925(request):
	J=',\n    ';B=request;C=B.GET.get('id');E=_G
	if C is _B:E=_A
	else:F=qube_cf975e3d38.sparta_c0fb6e4d66(C,B.user);E=not F[_K]
	if E:return sparta_6e5e202fc5(B)
	K=qube_cf975e3d38.sparta_7f995e4477(F[_E]);D='';G=0
	for(H,I)in K.items():
		if G>0:D+=J
		if I==1:D+=f"{H}=input_1"
		else:L=str(J.join([f"input_{A}"for A in range(I)]));D+=f"{H}=[{L}]"
		G+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_data(\n    "{C}",\n    {D}\n)';A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=7;O=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=F[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_8ffab28e13
def sparta_e9cc28df7f(request,session_id,api_token_id,json_vars_html):B=request;A=qube_ff414021cf.sparta_bce5bb4727(B);A[_C]=7;C=qube_ff414021cf.sparta_e8312e6c3f(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)
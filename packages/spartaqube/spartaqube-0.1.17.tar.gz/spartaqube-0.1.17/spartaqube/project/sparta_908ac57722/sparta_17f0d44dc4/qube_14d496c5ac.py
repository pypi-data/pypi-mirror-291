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
import project.sparta_addce897a6.sparta_cca83b7c2a.qube_bb2a0cc88d as qube_bb2a0cc88d
from project.sparta_866369bc29.sparta_a6cd567dfa.qube_bc116ca566 import sparta_9eee2d8f98
from project.sparta_866369bc29.sparta_fe661f0a14 import qube_f7a02eabc2 as qube_f7a02eabc2
@csrf_exempt
@sparta_9eee2d8f98
@login_required(redirect_field_name=_F)
def sparta_d66036f52e(request):
	B=request;C=B.GET.get('edit')
	if C is _B:C='-1'
	A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=7;D=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(D);A[_D]=_A;A['edit_chart_id']=C;return render(B,'dist/project/plot-db/plotDB.html',A)
@csrf_exempt
@sparta_9eee2d8f98
@login_required(redirect_field_name=_F)
def sparta_9a700a3569(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_f7a02eabc2.sparta_a2177a8814(C,A.user);D=not E[_K]
	if D:return sparta_d66036f52e(A)
	B=qube_bb2a0cc88d.sparta_a8bb6e74e5(A);B[_C]=7;F=qube_bb2a0cc88d.sparta_7e43fffad4(A.user);B.update(F);B[_D]=_A;B[_H]=C;G=E[_E];B[_I]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_9eee2d8f98
def sparta_0bbbf9f3db(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return sparta_ed1fbb3b6f(A,B)
@csrf_exempt
@sparta_9eee2d8f98
def sparta_3a280a5539(request,widget_id,session_id,api_token_id):return sparta_ed1fbb3b6f(request,widget_id,session_id)
def sparta_ed1fbb3b6f(request,plot_chart_id,session='-1'):
	G='res';E=plot_chart_id;B=request;C=_G
	if E is _B:C=_A
	else:
		D=qube_f7a02eabc2.sparta_407787c88f(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_d66036f52e(B)
	A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=7;I=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(I);A[_D]=_A;F=D[_E];A['b_require_password']=0 if D[G]==1 else 1;A[_H]=F.plot_chart_id;A[_I]=F.name;A[_J]=str(session);return render(B,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
@sparta_9eee2d8f98
def sparta_7ed912118c(request,session_id,api_token_id):B=request;A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=7;C=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_9eee2d8f98
@login_required(redirect_field_name=_F)
def sparta_3df6d6b9e4(request):
	J=',\n    ';B=request;C=B.GET.get('id');F=_G
	if C is _B:F=_A
	else:G=qube_f7a02eabc2.sparta_a2177a8814(C,B.user);F=not G[_K]
	if F:return sparta_d66036f52e(B)
	K=qube_f7a02eabc2.sparta_e517a0c101(G[_E]);D='';H=0
	for(E,I)in K.items():
		if H>0:D+=J
		if I==1:D+=f"{E}=input_{E}"
		else:L=str(J.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{L}]"
		H+=1
	M=f'Spartaqube().get_widget(\n    "{C}"\n)';N=f'Spartaqube().plot_(\n    "{C}",\n    {D}\n)';A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=7;O=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(O);A[_D]=_A;A[_H]=C;P=G[_E];A[_I]=P.name;A['plot_data_cmd']=M;A['plot_data_cmd_inputs']=N;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_9eee2d8f98
def sparta_f26658e0e5(request,session_id,api_token_id,json_vars_html):B=request;A=qube_bb2a0cc88d.sparta_a8bb6e74e5(B);A[_C]=7;C=qube_bb2a0cc88d.sparta_7e43fffad4(B.user);A.update(C);A[_D]=_A;A[_J]=session_id;A.update(json.loads(json_vars_html));return render(B,'dist/project/plot-db/plotAPI.html',A)
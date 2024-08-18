_B=True
_A=None
import os,json,platform,websocket,threading,time,pandas as pd
from project.sparta_993afa2e3a.sparta_80ae9d2234.qube_6f3f3a864f import IPythonKernel as IPythonKernel
from project.sparta_993afa2e3a.sparta_80ae9d2234.qube_622b233098 import sparta_28c091cbaa
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_581ca2ff5f import sparta_8b01070954,sparta_3637d48543
IS_WINDOWS=False
if platform.system()=='Windows':IS_WINDOWS=_B
from channels.generic.websocket import WebsocketConsumer
from project.sparta_06ab2796ce.sparta_6d86447bae import qube_ff414021cf as qube_ff414021cf
from project.sparta_993afa2e3a.sparta_28f2f63dd2 import qube_581ca2ff5f as qube_581ca2ff5f
class NotebookWS(WebsocketConsumer):
	channel_session=_B;http_user_and_session=_B
	def connect(A):print('Connect Now');A.accept();A.user=A.scope['user'];A.json_data_dict=dict();A.kernel_obj=_A
	def disconnect(A,close_code=_A):
		print('Disconnect');print('self.kernel_obj');print(A.kernel_obj)
		try:A.kernel_obj.stop_kernel()
		except Exception as B:print('Exception disconnect kernel');print(B)
		A.kernel_obj=_A
	def start_kernel(A):
		B=False
		if A.kernel_obj is _A:B=_B
		elif not A.kernel_obj.get_kernel_client().is_alive():B=_B;A.kernel_obj.stop_kernel()
		print('bStartIpythonKernel  > > > '+str(B))
		if B:A.kernel_obj=IPythonKernel()
	def receive(A,text_data):
		T='name';S='kernel_variable_arr';R='cell_id';Q='cellCode';M=text_data;L='cellId';H='value';G='res';F='service'
		if len(M)>0:
			C=json.loads(M);print(f"NOTEBOOK KERNEL json_data");print(C);B=C[F]
			if B=='init-socket'or B=='reconnect-kernel':E={G:1,F:B};A.start_kernel();D=json.dumps(E);A.send(text_data=D);return
			elif B=='disconnect':A.disconnect()
			elif B=='exec':
				if A.kernel_obj is _A:A.start_kernel()
				U=time.time();print('='*50);A.kernel_obj.execute(C[Q],websocket=A,cell_id=C[L])
				try:N=sparta_28c091cbaa(C[Q])
				except:N=[]
				print('='*50);V=time.time()-U;D=json.dumps({G:2,F:B,'elapsed_time':round(V,2),R:C[L],'updated_plot_variables':N});A.send(text_data=D)
			elif B=='reset':
				if A.kernel_obj is _A:A.start_kernel()
				A.kernel_obj.reset_kernel_workspace();E={G:1,F:B};D=json.dumps(E);A.send(text_data=D)
			elif B=='workspace-list':
				if A.kernel_obj is _A:A.start_kernel()
				W=A.kernel_obj.list_workspace_variables();E={G:1,F:B,'workspace_variables':W};E.update(C);D=json.dumps(E);A.send(text_data=D)
			elif B=='workspace-get-variable-as-df':
				if A.kernel_obj is _A:A.start_kernel()
				O=[];P=[]
				for I in C[S]:
					X=A.kernel_obj.get_workspace_variable(kernel_variable=I);J=sparta_8b01070954(X,variable_name=I);print('workspace_variable_df');print(J);print(type(J))
					try:O.append(sparta_3637d48543(J));P.append(I)
					except:pass
				E={G:1,F:B,S:P,'workspace_variable_arr':O};D=json.dumps(E);A.send(text_data=D)
			elif B=='workspace-get-variable'or B=='workspace-get-variable-preview':
				if A.kernel_obj is _A:A.start_kernel()
				Y=A.kernel_obj.get_kernel_variable_repr(kernel_variable=C['kernel_variable']);E={G:1,F:B,R:C.get(L,_A),'workspace_variable':Y};D=json.dumps(E);A.send(text_data=D)
			elif B=='workspace-set-variable-from-datasource':
				if A.kernel_obj is _A:A.start_kernel()
				if H in list(C.keys()):K=json.loads(C[H]);Z=pd.DataFrame(K['data'],columns=K['columns'],index=K['index']);A.kernel_obj.set_workspace_variable(name=C[T],value=Z);E={G:1,F:B};D=json.dumps(E);A.send(text_data=D)
			elif B=='workspace-set-variable':
				if A.kernel_obj is _A:A.start_kernel()
				if H in list(C.keys()):A.kernel_obj.set_workspace_variable(name=C[T],value=json.loads(C[H]));E={G:1,F:B};D=json.dumps(E);A.send(text_data=D)
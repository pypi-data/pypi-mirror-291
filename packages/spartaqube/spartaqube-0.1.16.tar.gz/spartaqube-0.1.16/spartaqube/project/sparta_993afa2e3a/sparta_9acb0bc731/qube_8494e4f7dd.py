_H='session_id'
_G='notebook_variables'
_F='errorMsg'
_E='session'
_D=False
_C=None
_B='utf-8'
_A='res'
import os,json,ast,base64,uuid,hashlib,cloudpickle
from random import randint
import pandas as pd
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared,CodeEditorNotebook
from project.models import ShareRights,UserProfile,NewPlotApiVariables
from project.sparta_993afa2e3a.sparta_8dad022c77 import qube_9adf7ad999 as qube_9adf7ad999
from project.sparta_993afa2e3a.sparta_44f1e7eacf import qube_cf975e3d38 as qube_cf975e3d38
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_581ca2ff5f import sparta_8b01070954,sparta_3637d48543
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_6d190f73e8 import sparta_f256ebe82f
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_6d190f73e8 import sparta_557ff95e6e
def sparta_3fc44a7ad1():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_2eef82f9f6():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_7081b1942d(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_6f387fe544(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(username='public_spartaqube').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_2eef82f9f6().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_f43b453cf4(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_2eef82f9f6().encode(_B));private_encryption=sparta_7081b1942d(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_3fc44a7ad1().encode(_B));public_encryption=sparta_7081b1942d(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_f2d8b1b5db(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_517301a782():plot_types=sparta_f256ebe82f();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_2bfa7b6afe(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_557ff95e6e(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_f4e72a86ac(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_0f94c5be84(json_data):
	user_code_example=json_data['userCode'];resp=_C;error_msg=''
	try:
		exec(user_code_example,globals(),locals());last_expression_str=sparta_f4e72a86ac(user_code_example)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			resp=json.dumps(resp);return{_A:1,'resp':resp,_F:error_msg}
	except Exception as e:return{_A:-1,_F:str(e)}
def sparta_c67608e046(json_data,user_obj):
	session_id=json_data[_E];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_8b01070954(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_3637d48543(notebook_variables_df))
		print(notebook_variables);return{_A:1,_G:notebook_variables}
	return{_A:-1}
def sparta_daa00d14f9(json_data,user_obj):session_id=json_data[_E];notebook_cached_variables=qube_cf975e3d38.sparta_483d458395(session_id);return{_A:1,_G:notebook_cached_variables}
def sparta_401abe035f(json_data,user_obj):session_id=json_data[_E];return qube_cf975e3d38.sparta_45d5c290c9(session_id)
def sparta_02e20df90f(json_data,user_obj):session_id=json_data[_E];widget_id=json_data['widgetId'];return qube_cf975e3d38.sparta_02e20df90f(user_obj,session_id,widget_id)
def sparta_2b8473223e(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_8703bf6ca2()
	elif api_service=='get_connectors':return sparta_968f99e858(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_46551b8c94(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_6273201f80(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_a21739b2ee(user_obj)
	elif api_service=='get_widget_data':return sparta_a1bbea33c1(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_f256ebe82f()
	elif api_service=='gui_plot_api_variables':return sparta_83837419ed(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_83837419ed(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_46ed6ae01b()
	return{_A:1,'output':output}
def sparta_8703bf6ca2():return 1
def sparta_968f99e858(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_cf975e3d38.sparta_89b08dc0b4(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_46551b8c94(json_data,user_obj):res_dict=qube_cf975e3d38.sparta_bf09b6e1b4(json_data,user_obj);return res_dict
def sparta_6273201f80(json_data,user_obj):res_dict=qube_cf975e3d38.sparta_1382b61b95(json_data,user_obj);return res_dict
def sparta_a21739b2ee(user_obj):return qube_cf975e3d38.sparta_091efb9f4a(user_obj)
def sparta_a1bbea33c1(json_data,user_obj):return qube_cf975e3d38.sparta_01bf06efde(json_data,user_obj)
def sparta_a9e9cc16e5(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_H:session_id}
def sparta_184b06aa16():return sparta_f256ebe82f()
def sparta_83837419ed(json_data,user_obj,b_check_type=True):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_f256ebe82f()]:return{_A:-1,_F:'Invalid chart_type input'}
	plot_params=json_data['plot_params'];all_hash_notebook=json_data['all_hash_notebook'];all_hash_server=json_data['all_hash_server'];b_missing_cache=_D
	for this_hash in all_hash_server:
		if cache.get(this_hash)is _C:b_missing_cache=True;break
	if b_missing_cache:
		cache_hash=[]
		for this_hash in all_hash_notebook:
			if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
		return{_A:-1,'status_service':1,A:cache_hash}
	session_id=str(uuid.uuid4());cache.set(session_id,plot_params,timeout=_C)
	for(key,val)in variables_dict.items():
		if isinstance(val,dict):
			hash=val['hash'];hash_value_cache=cache.get(hash)
			if hash_value_cache is _C:hash_value_input=val.get('var',_C);cache.set(hash,hash_value_input,timeout=_C);print(f"Set hash {hash} for {key}")
	cache_hash=[]
	for this_hash in all_hash_notebook:
		if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
	return{_A:1,_H:session_id,A:cache_hash}
def sparta_46ed6ae01b():cache.clear();return{_A:1}
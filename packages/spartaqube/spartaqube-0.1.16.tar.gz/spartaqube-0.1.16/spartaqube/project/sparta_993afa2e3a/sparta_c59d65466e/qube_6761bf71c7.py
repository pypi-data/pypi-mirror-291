import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_993afa2e3a.sparta_8dad022c77 import qube_9adf7ad999 as qube_9adf7ad999
from project.sparta_993afa2e3a.sparta_35cda80e40 import qube_6605b0caf0
from project.sparta_993afa2e3a.sparta_44f1e7eacf import qube_95876ff066 as qube_95876ff066
from project.sparta_993afa2e3a.sparta_35cda80e40.qube_d547dae498 import Connector as Connector
def sparta_dc88811e01(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_3b5f0d992f(B)
	return{'res':1,'output':C,D:B}
def sparta_3b5f0d992f(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]
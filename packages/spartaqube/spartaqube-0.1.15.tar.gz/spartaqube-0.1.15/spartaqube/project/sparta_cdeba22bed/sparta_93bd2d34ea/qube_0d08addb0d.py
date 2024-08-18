_D='manifest'
_C=None
_B=False
_A=True
import os,socket,json,requests
from datetime import date,datetime
from project.models import UserProfile,AppVersioning
from django.conf import settings as conf_settings
from spartaqube_app.secrets import sparta_b2d4724017
from project.sparta_d9c09478c6.sparta_8da5309606.qube_654d12f1a8 import sparta_9d948e68cf
import pytz
UTC=pytz.utc
class dotdict(dict):__getattr__=dict.get;__setattr__=dict.__setitem__;__delattr__=dict.__delitem__
def sparta_b2febc33d2(appViewsModels):
	A=appViewsModels
	if isinstance(A,list):
		for C in A:
			for B in list(C.keys()):
				if isinstance(C[B],date):C[B]=str(C[B])
	else:
		for B in list(A.keys()):
			if isinstance(A[B],date):A[B]=str(A[B])
	return A
def sparta_62c82887c4(thisText):A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=A+str('/log/log.txt');B=open(A,'a');B.write(thisText);B.writelines('\n');B.close()
def sparta_65e4d49ca8(request):A=request;return{'appName':'Project','user':A.user,'ip_address':A.META['REMOTE_ADDR']}
def sparta_d0bfc14378():return conf_settings.PLATFORM
def sparta_19b6063cc7():
	A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=os.path.dirname(os.path.dirname(A))
	if conf_settings.DEBUG:C='static'
	else:C='staticfiles'
	E=A+f"/{C}/dist/manifest.json";F=open(E);B=json.load(F)
	if conf_settings.B_TOOLBAR:
		G=list(B.keys())
		for D in G:B[D]=A+f"/{C}"+B[D]
	return B
def sparta_cdb85dde13(request):
	B='';C=''
	if len(B)>0:B='/'+str(B)
	if len(C)>0:C='/'+str(C)
	try:
		A=_B;F=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if F.count()==0:AppVersioning.objects.create(last_check_date=E);A=_A
		else:
			D=F[0];G=D.last_check_date;H=E-G;I=sparta_9d948e68cf();J=D.last_available_version_pip
			if not I==J:A=_A
			elif H.seconds>60*10:A=_A;D.last_check_date=E;D.save()
	except:A=_A
	K=conf_settings.HOST_WS_PREFIX;L=conf_settings.WEBSOCKET_PREFIX;M={'PROJECT_NAME':conf_settings.PROJECT_NAME,'CAPTCHA_SITEKEY':conf_settings.CAPTCHA_SITEKEY,'WEBSOCKET_PREFIX':L,'URL_PREFIX':B,'URL_WS_PREFIX':C,'HOST_WS_PREFIX':K,'CHECK_VERSIONING':A,'IS_DEV':conf_settings.IS_DEV};return M
def sparta_60c6b775bf(captcha):
	D='errorMsg';B='res';A=captcha
	try:
		if A is not _C:
			if len(A)>0:
				E=sparta_b2d4724017()['CAPTCHA_SECRET_KEY'];F=f"https://www.google.com/recaptcha/api/siteverify?secret={E}&response={A}";C=requests.get(F)
				if int(C.status_code)==200:
					G=json.loads(C.text)
					if G['success']:return{B:1}
	except Exception as H:return{B:-1,D:str(H)}
	return{B:-1,D:'Invalid captcha'}
def sparta_77fc7c8447(password):
	A=password;B=UserProfile.objects.filter(email=conf_settings.ADMIN_DEFAULT_EMAIL).all()
	if B.count()==0:return conf_settings.ADMIN_DEFAULT==A
	else:C=B[0];D=C.user;return D.check_password(A)
def sparta_3282d2cd9a(code):
	A=code
	try:
		if A is not _C:
			if len(A)>0:
				B=os.getenv('SPARTAQUBE_PASSWORD','admin')
				if B==A:return _A
	except:return _B
	return _B
def sparta_49252b01bd(user):
	F='default';A=dict()
	if not user.is_anonymous:
		E=UserProfile.objects.filter(user=user)
		if E.count()>0:
			B=E[0];D=B.avatar
			if D is not _C:D=B.avatar.avatar
			A['avatar']=D;A['userProfile']=B;C=B.editor_theme
			if C is _C:C=F
			elif len(C)==0:C=F
			else:C=B.editor_theme
			A['theme']=C;A['B_DARK_THEME']=B.is_dark_theme
	A[_D]=sparta_19b6063cc7();return A
def sparta_80f5384999(user):A=dict();A[_D]=sparta_19b6063cc7();return A
def sparta_088654ee5c():
	try:socket.create_connection(('1.1.1.1',53));return _A
	except OSError:pass
	return _B
def sparta_e187331a72():A=socket.gethostname();B=socket.gethostbyname(A);return A,B
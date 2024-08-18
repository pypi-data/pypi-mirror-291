_M='An error occurred, please try again'
_L='Invalid captcha'
_K='password_confirmation'
_J='password'
_I='jsonData'
_H='api_token_id'
_G='notLoggerAPI'
_F='is_created'
_E='utf-8'
_D='errorMsg'
_C=False
_B=True
_A='res'
import hashlib,re,uuid,json,requests,socket,base64,traceback
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout,login
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings as conf_settings
from django.urls import reverse
from project.models import UserProfile,GuestCode,GuestCodeGlobal,LocalApp,SpartaQubeCode
from project.sparta_cdeba22bed.sparta_93bd2d34ea.qube_0d08addb0d import sparta_60c6b775bf
from project.sparta_d9c09478c6.sparta_9103985536 import qube_9153d6a052 as qube_9153d6a052
from project.sparta_d9c09478c6.sparta_ece18d2157 import qube_93b3175200 as qube_93b3175200
from project.sparta_d9c09478c6.sparta_15b33bf63a.qube_744d3770b8 import Email as Email
def sparta_8eb9b85134(function):
	def A(request,*E,**C):
		A=request;B=_B
		if not A.user.is_active:B=_C;logout(A)
		if not A.user.is_authenticated:B=_C;logout(A)
		if not B:
			D=C.get(_H)
			if D is not None:F=qube_93b3175200.sparta_bc010829ea(D);login(A,F)
		return function(A,*E,**C)
	return A
def sparta_a937a5f24c(function):
	def A(request,*B,**C):
		A=request
		if not A.user.is_active:return HttpResponseRedirect(reverse(_G))
		if A.user.is_authenticated:return function(A,*B,**C)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_6ca9be0773(function):
	def A(request,*B,**C):
		try:return function(request,*B,**C)
		except Exception as A:
			if conf_settings.DEBUG:print('Try catch exception with error:');print(A);print('traceback:');print(traceback.format_exc())
			D={_A:-1,_D:str(A)};E=json.dumps(D);return HttpResponse(E)
	return A
def sparta_1fd5c24516(function):
	def A(request,*D,**E):
		A=request;B=_C
		try:
			F=json.loads(A.body);G=json.loads(F[_I]);H=G[_H];C=qube_93b3175200.sparta_bc010829ea(H)
			if C is not None:B=_B;A.user=C
		except Exception as I:print('exception pip auth');print(I)
		if B:return function(A,*D,**E)
		else:return HttpResponseRedirect(reverse(_G))
	return A
def sparta_b09bd36aa5(code):
	try:
		B=SpartaQubeCode.objects.all()
		if B.count()==0:return code=='admin'
		else:C=B[0].spartaqube_code;A=hashlib.md5(code.encode(_E)).hexdigest();A=base64.b64encode(A.encode(_E));A=A.decode(_E);return A==C
	except Exception as D:pass
	return _C
def sparta_e3cf5d4bec():
	A=LocalApp.objects.all()
	if A.count()==0:B=str(uuid.uuid4());LocalApp.objects.create(app_id=B,date_created=datetime.now());return B
	else:return A[0].app_id
def sparta_0aa13fe337():A=socket.gethostname();B=socket.gethostbyname(A);return B
def sparta_63e8683210(json_data):
	D='ip_addr';A=json_data;del A[_J];del A[_K]
	try:A[D]=sparta_0aa13fe337()
	except:A[D]=-1
	C=dict();C[_I]=json.dumps(A);B=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/create-user",data=json.dumps(C))
	if B.status_code==200:
		try:
			A=json.loads(B.text)
			if A[_A]==1:return{_A:1,_F:_B}
			else:A[_F]=_C;return A
		except Exception as E:return{_A:-1,_F:_C,_D:str(E)}
	return{_A:1,_F:_C,_D:f"status code: {B.status_code}. Please check your internet connection"}
def sparta_4725fd660b(json_data,hostname_url):
	O='emailExist';N='passwordConfirm';K='email';B=json_data;F={N:'The two passwords must be the same...',K:'Email address is not valid...','form':'The form you sent is not valid...',O:'This email is already registered...'};E=_C;P=B['firstName'].capitalize();Q=B['lastName'].capitalize();C=B[K].lower();L=B[_J];R=B[_K];S=B['code'];B['app_id']=sparta_e3cf5d4bec()
	if not sparta_b09bd36aa5(S):return{_A:-1,_D:'Invalid spartaqube code, please contact your administrator'}
	if L!=R:E=_B;G=F[N]
	if not re.match('[^@]+@[^@]+\\.[^@]+',C):E=_B;G=F[K]
	if User.objects.filter(username=C).exists():E=_B;G=F[O]
	if not E:
		T=sparta_63e8683210(B);M=_B;U=T[_F]
		if not U:M=_C
		A=User.objects.create_user(C,C,L);A.is_staff=_C;A.username=C;A.first_name=P;A.last_name=Q;A.is_active=_B;A.save();D=UserProfile(user=A);H=str(A.id)+'_'+str(A.email);H=H.encode(_E);I=hashlib.md5(H).hexdigest()+str(datetime.now());I=I.encode(_E);V=str(uuid.uuid4());D.user_profile_id=hashlib.sha256(I).hexdigest();D.email=C;D.api_key=str(uuid.uuid4());D.registration_token=V;D.b_created_website=M;D.save();J={_A:1,'userObj':A};return J
	J={_A:-1,_D:G};return J
def sparta_2f7d3d113b(user_obj,hostname_url,registration_token):C='Validate your account';B=user_obj;A=Email(B.username,[B.email],f"Welcome to {conf_settings.PROJECT_NAME}",C);A.addOneRow(C);A.addSpaceSeparator();A.addOneRow('Click on the link below to validate your account');D=f"{hostname_url.rstrip('/')}/registration-validation/{registration_token}";A.addOneCenteredButton('Validate',D);A.send()
def sparta_ede5a927c9(token):
	C=UserProfile.objects.filter(registration_token=token)
	if C.count()>0:A=C[0];A.registration_token='';A.is_account_validated=_B;A.save();B=A.user;B.is_active=_B;B.save();return{_A:1,'user':B}
	return{_A:-1,_D:'Invalid registration token'}
def sparta_d44f2c6719():return conf_settings.IS_GUEST_CODE_REQUIRED
def sparta_5e78a434ca(guest_code):
	if GuestCodeGlobal.objects.filter(guest_id=guest_code,is_active=_B).count()>0:return _B
	return _C
def sparta_97e98cde9a(guest_code,user_obj):
	D=user_obj;C=guest_code
	if GuestCodeGlobal.objects.filter(guest_id=C,is_active=_B).count()>0:return _B
	A=GuestCode.objects.filter(user=D)
	if A.count()>0:return _B
	else:
		A=GuestCode.objects.filter(guest_id=C,is_used=_C)
		if A.count()>0:B=A[0];B.user=D;B.is_used=_B;B.save();return _B
	return _C
def sparta_ab024ea397(user):
	A=UserProfile.objects.filter(user=user)
	if A.count()==1:return A[0].is_banned
	else:return _C
def sparta_78cad2043d(email,captcha):
	D=sparta_60c6b775bf(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0];C=str(uuid.uuid4());A.token_reset_password=C;A.save();sparta_7cb41ff4b2(A.user,C);return{_A:1}
def sparta_7cb41ff4b2(user_obj,token_reset_password):B=user_obj;A=Email(B.username,[B.email],'Reset Password','Reset Password Message');A.addOneRow('Reset code','Copy the following code to reset your password');A.addSpaceSeparator();A.addOneRow(token_reset_password);A.send()
def sparta_f0a4a2b1f0(captcha,token,email,password):
	D=sparta_60c6b775bf(captcha)
	if D[_A]!=1:return{_A:-1,_D:_L}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_M}
	A=B[0]
	if not token==A.token_reset_password:return{_A:-1,_D:'Invalid token..., please try again'}
	A.token_reset_password='';A.save();C=A.user;C.set_password(password);C.save();return{_A:1}
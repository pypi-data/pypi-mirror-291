_I='name'
_H='universe_id'
_G='ptf_id'
_F='shareType'
_E='user'
_D='type'
_C=None
_B='res'
_A=False
import json,base64,hashlib,re,uuid,pandas as pd
from datetime import datetime,timedelta
from dateutil import parser
import pytz
UTC=pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import User,UserProfile,UserGroup,UserGroupUser,ShareRights,notificationShare
from project.sparta_d9c09478c6.sparta_6dea060a26 import qube_3c49e6f2a3 as qube_3c49e6f2a3
from project.sparta_d9c09478c6.sparta_2e9bac4212 import qube_d1cc48ac8f as qube_d1cc48ac8f
def sparta_470332878d(json_data,userObj):
	G='value';A=json_data['query'];A=A.lower();B=[];H=UserProfile.objects.filter(Q(user__first_name__icontains=A)|Q(user__last_name__icontains=A)).all()[0:6]
	for C in H:
		D=C.user
		if userObj==D:continue
		I=C.avatar;E='-1'
		if I is not _C:E=C.avatarObj.image64
		B.append({_I:D.first_name+' '+str(D.last_name),G:C.user_profile_id,'image64':E,_D:_E})
	J=UserGroup.objects.filter(name__icontains=A,is_delete=_A).all()[0:6]
	for F in J:B.append({_I:F.name,G:F.groupId,_D:'group'})
	K={_B:1,'members':B,'nbRes':len(B)};return K
def sparta_e56c59a05e(json_data,user_obj):
	U='bAdminMe';T='bReshareMe';S='bWriteMe';R='nbDependencies';P='resDependenciesDict';E=json_data;A=user_obj;M=int(E[_F])
	if M==0:
		V=E[_G];N=Portfolio.objects.filter(ptf_id=V,is_delete=_A).all()
		if N.count()==1:
			F=N[0];G=qube_3c49e6f2a3.sparta_d93e0670f7(A);C=[A.userGroup for A in G]
			if len(C)>0:H=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=C,portfolio=F)&~Q(portfolio__user=A)|Q(is_delete=0,user=A,portfolio=F))
			else:H=PortfolioShared.objects.filter(is_delete=0,user=A,portfolio=F)
			if H.count()>0:W=H[0];B=W.ShareRights;D=[];I=len(D);J={_B:1,P:D,R:I,S:B.has_write_rights,T:B.has_reshare_rights,U:B.is_admin};return J
	elif M==1:
		X=E[_H];O=Universe.objects.filter(universe_id=X,is_delete=_A).all()
		if O.count()==1:
			K=O[0];G=qube_3c49e6f2a3.sparta_d93e0670f7(A);C=[A.userGroup for A in G]
			if len(C)>0:L=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=C,universe=K)&~Q(universe__user=A)|Q(is_delete=0,user=A,universe=K))
			else:L=UniverseShared.objects.filter(is_delete=0,user=A,universe=K)
			if L.count()>0:Y=L[0];B=Y.shareRights;D=[];I=len(D);J={_B:1,P:D,R:I,S:B.has_write_rights,T:B.has_reshare_rights,U:B.is_admin};return J
	return{_B:-1}
def sparta_4186e914eb(json_data,user_obj):
	F=json_data;A=user_obj;G=[];K=[];L=int(F[_F])
	if L==0:
		S=F[_G];M=Portfolio.objects.filter(ptf_id=S,is_delete=_A).all()
		if M.count()==1:
			D=M[0];H=qube_3c49e6f2a3.sparta_d93e0670f7(A);C=[A.userGroup for A in H]
			if len(C)>0:I=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=C,portfolio=D)&~Q(portfolio__user=A)|Q(is_delete=0,user=A,portfolio=D))
			else:I=PortfolioShared.objects.filter(is_delete=0,user=A,portfolio=D)
			if I.count()>0:
				T=I[0]
				if T.ShareRights.is_admin:G=PortfolioShared.objects.filter(is_delete=_A,portfolio=D)
	elif L==1:
		U=F[_H];N=Universe.objects.filter(universe_id=U,is_delete=_A).all()
		if N.count()==1:
			E=N[0];H=qube_3c49e6f2a3.sparta_d93e0670f7(A);C=[A.userGroup for A in H]
			if len(C)>0:J=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=C,universe=E)&~Q(universe__user=A)|Q(is_delete=0,user=A,universe=E))
			else:J=UniverseShared.objects.filter(is_delete=0,user=A,universe=E)
			if J.count()>0:
				V=J[0]
				if V.ShareRights.is_admin:G=UniverseShared.objects.filter(is_delete=_A,universe=E)
	for B in G:
		O=_A
		if B.userGroup is not _C:P=1;R=B.userGroup.name
		else:P=0;R=B.user.first_name+' '+B.user.last_name;O=B.shareRights.is_admin
		if not O:W={'groupAccessType':P,_I:R,'bWrite':int(B.ShareRights.has_write_rights),'bReshare':int(B.ShareRights.has_reshare_rights),'idShared':B.id};K.append(W)
	X={_B:1,'arrRes':K};return X
def sparta_91c2a74b41(json_data,user_obj):
	Y='Your are not allowed to share this object';X='errorMsg';R='member';J=json_data;B=user_obj;print('json_data SHARE OBJECTS');print(J);L=datetime.now().astimezone(UTC);P=qube_3c49e6f2a3.sparta_d93e0670f7(B);M=[A.userGroup for A in P];U=J['member2ShareArr'];I=int(J[_F])
	def N(shareRightsObj):
		A=shareRightsObj;B=J['bWritePrivilege'];C=J['bResharePrivilege']
		if A is not _C:
			D=A.has_write_rights;E=A.has_reshare_rights
			if not D:B=_A
			if not E:C=_A
		F=ShareRights.objects.create(is_admin=_A,has_write_rights=B,has_reshare_rights=C,last_update=L);return F
	def O(thisMember,share_type,userOrUserGroup,obj):
		D=userOrUserGroup;C=share_type
		def E(this_user):
			A=notificationShare.objects.create(type_object=C,user=this_user,user_from=B,date_created=L)
			if C==0:A.portfolio=obj
			elif C==1:A.universe=obj
			A.save()
		if thisMember[_D]==_E:E(D)
		else:
			F=UserGroupUser.objects.filter(is_delete=_A,userGroup=D)
			if F.count()>0:
				for G in F:
					A=G.user;print('thisUser > ');print(A);print(A.username)
					if not A==B:E(A)
	if I==0:
		Z=J[_G];V=Portfolio.objects.filter(ptf_id=Z,is_delete=_A).all()
		if V.count()==1:
			C=V[0];P=qube_3c49e6f2a3.sparta_d93e0670f7(B);M=[A.userGroup for A in P]
			if len(M)>0:S=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=M,portfolio=C)&~Q(portfolio__user=B)|Q(is_delete=0,user=B,portfolio=C))
			else:S=PortfolioShared.objects.filter(is_delete=0,user=B,portfolio=C)
			if S.count()>0:
				a=S[0];E=a.ShareRights
				if not E.has_reshare_rights:return{_B:-1,X:Y}
				for A in U:
					if A[_D]==_E:
						F=UserProfile.objects.get(user_profile_id=A[R]);G=PortfolioShared.objects.filter(user=F.user,portfolio=C)
						if G.count()==0:PortfolioShared.objects.create(portfolio=C,user=F.user,dateCreated=L,shareRights=N(E));O(A,I,F.user,C)
						else:
							H=G[0]
							if H.is_delete:H.is_delete=_A;H.ShareRights=N(E);H.save();O(A,I,F.user,C)
					else:
						K=UserGroup.objects.get(groupId=A[R]);G=PortfolioShared.objects.filter(user_group=K,portfolio=C)
						if G.count()==0:PortfolioShared.objects.create(portfolio=C,userGroup=K,dateCreated=L,shareRights=N(E));O(A,I,K,C)
	elif I==1:
		b=J[_H];W=Universe.objects.filter(universe_id=b,is_delete=_A).all()
		if W.count()==1:
			D=W[0];P=qube_3c49e6f2a3.sparta_d93e0670f7(B);M=[A.userGroup for A in P]
			if len(M)>0:T=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=M,universe=D)&~Q(universe__user=B)|Q(is_delete=0,user=B,universe=D))
			else:T=UniverseShared.objects.filter(is_delete=0,user=B,universe=D)
			if T.count()>0:
				c=T[0];E=c.ShareRights
				if not E.has_reshare_rights:return{_B:-1,X:Y}
				for A in U:
					if A[_D]==_E:
						F=UserProfile.objects.get(user_profile_id=A[R]);G=UniverseShared.objects.filter(user=F.user,universe=D)
						if G.count()==0:UniverseShared.objects.create(universe=D,user=F.user,dateCreated=L,shareRights=N(E));O(A,I,F.user,D)
						else:
							H=G[0]
							if H.is_delete:H.is_delete=_A;H.ShareRights=N(E);H.save();O(A,I,F.user,D)
					else:
						K=UserGroup.objects.get(groupId=A[R]);G=PortfolioShared.objects.filter(user_group=K,universe=D)
						if G.count()==0:UniverseShared.objects.create(universe=D,userGroup=K,dateCreated=L,shareRights=N(E));O(A,I,K,D)
	return{_B:1}
def sparta_969eb6ccf9(json_data,user_obj):
	A=json_data;print('setSharePrivileges');print(A);D=int(A[_F]);E=A['idSharedObj'];F=bool(A['rightsVal']);G=int(A['typePrivilege']);B=_C
	if D==0:
		J=A[_G];H=Portfolio.objects.filter(ptf_id=J,is_delete=_A)
		if H.count()>0:K=H[0];B=PortfolioShared.objects.filter(is_delete=0,portfolio=K,id=E)
	elif D==1:
		L=A[_H];I=Universe.objects.filter(universe_id=L,is_delete=_A)
		if I.count()>0:M=I[0];B=UniverseShared.objects.filter(is_delete=0,universe=M,id=E)
	if B is not _C:
		if B.count()>0:
			N=B[0];C=N.ShareRights
			if G==0:C.has_write_rights=F
			elif G==1:C.has_reshare_rights=F
			C.save()
	O={_B:1};return O
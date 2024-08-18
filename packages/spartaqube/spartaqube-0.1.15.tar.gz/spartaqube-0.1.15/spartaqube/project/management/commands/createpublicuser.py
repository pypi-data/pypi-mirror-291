import uuid,hashlib,time
from datetime import datetime
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from project.models import UserProfile
class Command(BaseCommand):
	help='Create a public user'
	def handle(J,*K,**L):
		G='utf-8';C='public_spartaqube';F='public@spartaqube.com';H='public'
		if not User.objects.filter(username=C).exists():A=User.objects.create_user(username=C,email=F,password=H)
		else:A=User.objects.filter(username=C).all()[0]
		if not UserProfile.objects.filter(user=A).exists():B=UserProfile(user=A);D=str(A.id)+'_'+str(A.email);D=D.encode(G);E=hashlib.md5(D).hexdigest()+str(datetime.now());E=E.encode(G);I=str(uuid.uuid4());B.user_profile_id=hashlib.sha256(E).hexdigest();B.email=F;B.api_key=str(uuid.uuid4());B.registration_token=I;B.save()
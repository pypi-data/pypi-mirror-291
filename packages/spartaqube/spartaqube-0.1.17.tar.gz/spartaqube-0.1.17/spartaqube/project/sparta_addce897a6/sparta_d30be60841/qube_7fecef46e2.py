import os
from project.sparta_addce897a6.sparta_d30be60841.qube_deb000c5e1 import qube_deb000c5e1
from project.sparta_addce897a6.sparta_d30be60841.qube_297cdb3437 import qube_297cdb3437
from project.sparta_addce897a6.sparta_d30be60841.qube_51028e15db import qube_51028e15db
from project.sparta_addce897a6.sparta_d30be60841.qube_e1119a2bb1 import qube_e1119a2bb1
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_deb000c5e1()
		elif A.dbType==1:A.dbCon=qube_297cdb3437()
		elif A.dbType==2:A.dbCon=qube_51028e15db()
		elif A.dbType==4:A.dbCon=qube_e1119a2bb1()
		return A.dbCon
import os
from project.sparta_06ab2796ce.sparta_d1bff634ab.qube_dc6b420377 import qube_dc6b420377
from project.sparta_06ab2796ce.sparta_d1bff634ab.qube_dbac1b684a import qube_dbac1b684a
from project.sparta_06ab2796ce.sparta_d1bff634ab.qube_7a467c1632 import qube_7a467c1632
from project.sparta_06ab2796ce.sparta_d1bff634ab.qube_8a36ce5aa7 import qube_8a36ce5aa7
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_dc6b420377()
		elif A.dbType==1:A.dbCon=qube_dbac1b684a()
		elif A.dbType==2:A.dbCon=qube_7a467c1632()
		elif A.dbType==4:A.dbCon=qube_8a36ce5aa7()
		return A.dbCon
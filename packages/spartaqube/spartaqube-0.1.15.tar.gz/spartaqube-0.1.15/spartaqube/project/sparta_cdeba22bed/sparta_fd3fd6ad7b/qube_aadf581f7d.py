import os
from project.sparta_cdeba22bed.sparta_fd3fd6ad7b.qube_76b8f84fb2 import qube_76b8f84fb2
from project.sparta_cdeba22bed.sparta_fd3fd6ad7b.qube_437e877385 import qube_437e877385
from project.sparta_cdeba22bed.sparta_fd3fd6ad7b.qube_fdabe83727 import qube_fdabe83727
from project.sparta_cdeba22bed.sparta_fd3fd6ad7b.qube_931b995a1d import qube_931b995a1d
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_76b8f84fb2()
		elif A.dbType==1:A.dbCon=qube_437e877385()
		elif A.dbType==2:A.dbCon=qube_fdabe83727()
		elif A.dbType==4:A.dbCon=qube_931b995a1d()
		return A.dbCon
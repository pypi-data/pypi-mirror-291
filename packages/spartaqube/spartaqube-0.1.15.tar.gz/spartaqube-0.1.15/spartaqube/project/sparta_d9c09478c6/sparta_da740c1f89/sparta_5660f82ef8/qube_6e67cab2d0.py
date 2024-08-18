import time
from project.sparta_d9c09478c6.sparta_da740c1f89.qube_b4d54ce7bf import EngineBuilder
class MysqlConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mysql');A.connector=A.build_mysql()
	def test_connection(A):
		B=False
		try:
			if A.connector.is_connected():A.connector.close();return True
			else:return B
		except Exception as C:print(f"Error: {C}");return B
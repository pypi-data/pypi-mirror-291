_D='There was a problem with Oracle'
_C=True
_B=False
_A=None
import cx_Oracle,pandas as pd
from project.sparta_d9c09478c6.sparta_da740c1f89.qube_b4d54ce7bf import EngineBuilder
from project.sparta_d9c09478c6.sparta_b184892b51.qube_8a75fefeff import sparta_8be9597829
class OracleConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database=_A,lib_dir=_A,oracle_service_name='orcl'):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='oracle+cx_oracle');A.connector=A.build_oracle(lib_dir,oracle_service_name)
	def test_connection(A):
		C=A.connector;D=_B
		try:
			B=C.cursor();E=_B
			if A.database is not _A:
				if len(A.database)>0:E=_C
			if E:F=A.database;B.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {F}")
			B.execute("SELECT 'Connection successful' FROM dual");H=B.fetchone();D=_C
		except cx_Oracle.DatabaseError as G:A.error_msg_test_connection=str(G)
		finally:
			if B:B.close()
			if C:C.close()
		return D
	def get_available_tables(B):
		C=B.connector;D=[]
		try:
			A=C.cursor();E=_B
			if B.database is not _A:
				if len(B.database)>0:E=_C
			if E:F=B.database;A.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {F}")
			A.execute('SELECT table_name FROM user_tables');G=A.fetchall();D=[A[0]for A in G]
		except cx_Oracle.DatabaseError as H:print(_D,H)
		finally:
			if A:A.close()
			if C:C.close()
		return D
	def get_table_columns(B,table_name):
		C=B.connector;D=[]
		try:
			A=C.cursor();E=_B
			if B.database is not _A:
				if len(B.database)>0:E=_C
			if E:F=B.database;A.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {F}")
			A.execute('\n                SELECT column_name \n                FROM all_tab_columns \n                WHERE table_name = :table_name\n            ',table_name=table_name);G=A.fetchall();D=[A[0]for A in G]
		except cx_Oracle.DatabaseError as H:print(_D,H)
		finally:
			if A:A.close()
			if C:C.close()
		return D
	def get_data_table(B,table_name):
		C=B.connector;D=_A;E=_A
		try:
			A=C.cursor();F=_B
			if B.database is not _A:
				if len(B.database)>0:F=_C
			if F:H=B.database;A.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {H}")
			A.execute(f"SELECT * FROM {table_name}");I=A.fetchall();J=[A[0]for A in A.description];D=[dict(zip(J,A))for A in I]
		except cx_Oracle.DatabaseError as G:print(_D,G);E=G
		finally:
			if A:A.close()
			if C:C.close()
		if D is not _A:return sparta_8be9597829(D)
		raise Exception(E)
	def get_data_table_query(B,sql,table_name=_A):
		C=B.connector;D=_A;E=_A
		try:
			A=C.cursor();F=_B
			if B.database is not _A:
				if len(B.database)>0:F=_C
			if F:H=B.database;A.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {H}")
			A.execute(sql);I=A.fetchall();J=[A[0]for A in A.description];D=[dict(zip(J,A))for A in I]
		except cx_Oracle.DatabaseError as G:print(_D,G);E=G
		finally:
			if A:A.close()
			if C:C.close()
		if D is not _A:return sparta_8be9597829(D)
		raise Exception(E)
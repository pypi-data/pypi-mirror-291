_A=None
import arcticdb as adb,pandas as pd
from project.sparta_993afa2e3a.sparta_35cda80e40.qube_8bea6ce306 import EngineBuilder
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_581ca2ff5f import sparta_8b01070954
class ArcticConnector(EngineBuilder):
	def __init__(A,database_path,library_arctic):
		C=library_arctic;B=database_path;A.database_path=B;A.library_arctic=C;super().__init__(host=_A,port=_A,engine_name='arctic')
		try:A.connector=A.build_arctic(B,C)
		except:A.connector=_A
	def test_connection(A):
		D='Missing library';C='Missing path or endpoint';B=False
		if A.database_path is _A:A.error_msg_test_connection=C;return B
		if len(A.database_path)==0:A.error_msg_test_connection=C;return B
		if A.library_arctic is _A:A.error_msg_test_connection=D;return B
		if len(A.library_arctic)==0:A.error_msg_test_connection=D;return B
		try:
			E=A.connector
			if A.library_arctic in E.list_libraries():return True
			else:A.error_msg_test_connection='Invalid path folder, endpoint or library';return B
		except Exception as F:A.error_msg_test_connection=str(F);return B
	def get_available_tables(A):
		try:B=A.connector;C=B[A.library_arctic];return list(C.list_symbols())
		except Exception as D:A.error_msg_test_connection=str(D);return[]
	def get_table_columns(A,table_name):
		try:B=A.connector;C=B[A.library_arctic];D=C.read_metadata(table_name);E=D['schema']['fields'];F=[A['name']for A in E];return F
		except Exception as G:A.error_msg_test_connection=str(G);return[]
	def get_data_table(A,table_name):B=A.connector;C=B[A.library_arctic];return sparta_8b01070954(C.read(table_name).data)
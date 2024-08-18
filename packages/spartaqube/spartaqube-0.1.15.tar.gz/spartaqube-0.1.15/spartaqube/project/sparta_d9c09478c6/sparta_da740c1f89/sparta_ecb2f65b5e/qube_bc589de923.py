_A=False
import os,re,openpyxl,duckdb,pandas as pd
from project.sparta_d9c09478c6.sparta_da740c1f89.qube_b4d54ce7bf import EngineBuilder
class ParquetConnector(EngineBuilder):
	def __init__(A,database_path):B=database_path;super().__init__(host=None,port=None,engine_name='parquet');A.database=B;A.connector=A.build_parquet(database_path=B)
	def test_connection(A):
		try:
			if os.path.isfile(A.database):return True
			else:return _A
		except Exception as B:print(f"Error: {B}");A.error_msg_test_connection=str(B);return _A
	def get_available_tables(A):
		def C(file_path):A=os.path.basename(file_path);B=os.path.splitext(A)[0];return B
		try:
			if os.path.isfile(A.database):return[C(A.database)]
			else:return[]
		except Exception as B:print(f"Error: {B}");A.error_msg_test_connection=str(B);return _A
	def get_table_columns(A,table_name):
		try:B=f"PRAGMA table_info('{A.database}')";C=A.connector.execute(B).fetchdf();D=C['name'].tolist();return D
		except Exception as E:print(f"Failed to list columns for table '{table_name}': {E}");return[]
	def get_data_table(A,table_name):
		try:B=f"SELECT * FROM '{A.database}'";C=A.connector.execute(B).fetchdf();return C
		except Exception as D:raise Exception(D)
	def get_data_table_query(C,sql,table_name=None):
		B='SQ_PARQUET'
		def D(sql_query):A=sql_query;A=re.sub('--.*','',A);A=re.sub('#.*','',A);A=re.sub('/\\*.*?\\*/','',A,flags=re.DOTALL);A=' '.join(A.split());return A
		try:A=sql;A=A.replace('"SQ_PARQUET"',B);A=A.replace("'SQ_PARQUET'",B);A=A.replace(B,f"'{C.database}'");A=D(A);E=C.connector.execute(A).fetchdf();return E
		except Exception as F:raise Exception(F)
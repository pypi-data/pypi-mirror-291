import pandas as pd
from project.sparta_993afa2e3a.sparta_35cda80e40.qube_8bea6ce306 import EngineBuilder
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_581ca2ff5f import sparta_8b01070954
class ScylladbConnector(EngineBuilder):
	def __init__(A,host,port,user,password,keyspace):C=password;B=keyspace;A.keyspace=B;super().__init__(host=host,port=port,user=user,password=C,engine_name='scylladb');A.set_url_engine(f"cassandra://{user}:{C}@{host}:{port}/{B}");A.cluster=A.build_scylladb(A.keyspace);A.connector=A.cluster.connect(B);A.connector.set_keyspace(B)
	def test_connection(A):
		C=False
		try:
			D=A.connector;E=D.execute('SELECT keyspace_name FROM system_schema.keyspaces');F=[A.keyspace_name for A in E]
			if A.keyspace in F:B=True
			else:A.error_msg_test_connection=f"Keyspace '{A.keyspace}' does not exist";B=C
			A.cluster.shutdown();return B
		except Exception as G:A.error_msg_test_connection=str(G);return C
	def get_available_tables(A):
		try:B=A.connector;C=f"SELECT table_name FROM system_schema.tables WHERE keyspace_name='{A.keyspace}'";D=B.execute(C);E=[A.table_name for A in D];A.cluster.shutdown();return E
		except Exception as F:A.error_msg_test_connection=str(F);return[]
	def get_table_columns(A,table_name):
		try:B=A.connector;C=f"SELECT column_name FROM system_schema.columns WHERE keyspace_name={A.keyspace} AND table_name={table_name}";D=B.execute(C);E=[A.column_name for A in D];A.cluster.shutdown();return E
		except Exception as F:A.error_msg_test_connection=str(F);return[]
	def get_data_table(A,table_name):
		try:B=A.connector;C=f"SELECT * FROM {table_name}";D=B.execute(C);E=[dict(A._asdict())for A in D];return sparta_8b01070954(E)
		except Exception as F:A.cluster.shutdown();raise Exception(F)
	def get_data_table_query(A,sql,table_name=None):
		try:B=A.connector;C=sql;D=B.execute(C);E=[dict(A._asdict())for A in D];return sparta_8b01070954(E)
		except Exception as F:A.cluster.shutdown();raise Exception(F)
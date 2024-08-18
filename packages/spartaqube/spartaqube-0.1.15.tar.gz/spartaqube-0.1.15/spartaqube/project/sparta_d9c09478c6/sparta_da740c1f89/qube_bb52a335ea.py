_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_d9c09478c6.sparta_da740c1f89.qube_926b6e1879 as qube_926b6e1879
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_e9b476669f.qube_0d23618231 import ArcticConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_d2542cd19e.qube_db97cce8b8 import AerospikeConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_1141b2756d.qube_510f3044de import CassandraConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_4ecca6eb16.qube_e7cb9719d7 import ClickhouseConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_2a0eecea0d.qube_d4e92fdfca import CouchdbConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_059026696c.qube_dfdb989e4e import CsvConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_7786b049fc.qube_1c8d8d36d2 import DuckDBConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_b3436bf6af.qube_bb2cba875c import JsonApiConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_9a85242db3.qube_17d1016104 import InfluxdbConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_99899bbe15.qube_ad6c69f98f import MariadbConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_73dfbcd7c5.qube_4d0e97eac6 import MongoConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_88dd874510.qube_8d055ce75e import MssqlConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_5660f82ef8.qube_6e67cab2d0 import MysqlConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_3cc9114ba8.qube_bb9664842b import OracleConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_ecb2f65b5e.qube_bc589de923 import ParquetConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_a937a05d21.qube_8ecd68d36b import PostgresConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_aac4cb248a.qube_7b2ce547f0 import PythonConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_e239834e04.qube_ac128e432e import QuestDBConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_2eb7ab8c99.qube_dbf86c1faf import RedisConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_eb3fe88328.qube_5d08928900 import ScylladbConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_940cbccca2.qube_88f3b6343b import SqliteConnector
from project.sparta_d9c09478c6.sparta_da740c1f89.sparta_7426e1707f.qube_332fe8bf2f import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_926b6e1879.sparta_1b68fc463e(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host;print('self.db_engine > '+str(A.db_engine))
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='arctic':A.db_connector=ArcticConnector(database_path=G,library_arctic=library_arctic)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_243e07f12d(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)
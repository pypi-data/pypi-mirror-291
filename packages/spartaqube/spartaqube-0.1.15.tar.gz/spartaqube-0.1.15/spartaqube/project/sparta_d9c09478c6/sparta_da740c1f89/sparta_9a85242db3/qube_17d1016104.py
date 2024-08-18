_B='measurement'
_A=None
import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from project.sparta_d9c09478c6.sparta_da740c1f89.qube_b4d54ce7bf import EngineBuilder
from project.sparta_d9c09478c6.sparta_b184892b51.qube_8a75fefeff import sparta_8be9597829
class InfluxdbConnector(EngineBuilder):
	def __init__(A,host,port,token,organization,bucket,user=_A,password=_A):
		E=password;D=organization;C=token;B=host
		if B.startswith('localhost'):B='http://localhost'
		super().__init__(host=B,port=port,engine_name='influxdb');A.connector=A.build_influxdb(C,D,user,E);A.bucket=bucket;A.token=C;A.organization=D;A.user=user;A.password=E
	def test_connection(A):
		G=False;D=G
		try:
			E=f"{A.host}:{A.port}";B=_A
			if A.token is not _A:
				if len(A.token)>0:B=InfluxDBClient(url=E,token=A.token,org=A.organization)
			if B is _A:
				if A.user is not _A:
					if len(A.user)>0:B=InfluxDBClient(url=E,username=A.user,password=A.password,org=A.organization)
			if B is _A:D=G;A.error_msg_test_connection='Either token with org or username with password must be provided.'
			else:
				try:H=B.query_api();I=f'from(bucket: "{A.bucket}") |> range(start: -1h)';J=H.query(I);D=True
				except Exception as C:A.error_msg_test_connection=str(C)
		except InfluxDBError as C:A.error_msg_test_connection=str(C);print('Failed to connect to InfluxDB:',C)
		except ValueError as F:A.error_msg_test_connection=str(F);print(F)
		finally:
			if B is not _A:B.close()
		return D
	def get_available_buckets(B):
		try:A=B.connector;C=A.buckets_api();D=C.find_buckets().buckets;E=[A.name for A in D];return E
		except InfluxDBError as F:print('Failed to list buckets:',F);return[]
		finally:A.close()
	def get_available_tables(A):
		try:B=A.connector;C=B.query_api();D=f'import "influxdata/influxdb/schema" schema.measurements(bucket: "{A.bucket}")';E=C.query(D,org=A.organization);F=[B.get_value()for A in E for B in A.records];return F
		except InfluxDBError as G:print('Failed to list measurements from the bucket:',G);return[]
		finally:B.close()
	def get_table_columns(A,table_name):
		C=table_name
		try:B=A.connector;D=B.query_api();E=f'''
            import "influxdata/influxdb/schema"
            schema.fieldKeys(
            bucket: "{A.bucket}",
            predicate: (r) => r._measurement == "{C}"
            )
            ''';F=D.query(E,org=A.organization);G=[B.get_value()for A in F for B in A.records];return G
		except InfluxDBError as H:print('Failed to list columns from the measurement:',H);return[]
		finally:B.close()
	def get_data_table(B,table_name):
		E=table_name
		try:
			C=B.connector;F=C.query_api();G=f'\n            from(bucket: "{B.bucket}")\n            |> range(start: 0)\n            |> filter(fn: (r) => r._measurement == "{E}")\n            ';H=F.query(G,org=B.organization);D=[]
			for I in H:
				for A in I.records:D.append({'time':A.get_time(),_B:A.get_measurement(),'field':A.get_field(),'value':A.get_value(),'tags':A.values})
			return sparta_8be9597829(D)
		except InfluxDBError as J:print('Failed to query data from the measurement:',J);return[]
		finally:C.close()
	def get_data_table_query(B,sql,table_name=_A):
		C=sql;K=table_name;D=B.connector;G=D.query_api();E=C.split('\n');E=[A for A in E if len(A)>0];C=''.join([A for A in E if A[0]!='#']);H=f'from(bucket: "{B.bucket}") {C}';I=G.query(H,org=B.organization);F=[]
		for J in I:
			for A in J.records:F.append({'time':A.get_time(),_B:A.get_measurement(),'field':A.get_field(),'value':A.get_value(),'tags':A.values})
		if D is not _A:D.close()
		if len(F)>0:return sparta_8be9597829(F)
		else:return pd.DataFrame()
import aerospike,pandas as pd
from project.sparta_993afa2e3a.sparta_35cda80e40.qube_8bea6ce306 import EngineBuilder
from project.sparta_993afa2e3a.sparta_28f2f63dd2.qube_581ca2ff5f import sparta_8b01070954
class AerospikeConnector(EngineBuilder):
	def __init__(self,host,port,user,password,database=None):port=int(port);super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='aerospike');self.connector=self.build_aerospike()
	def test_connection(self):
		A=False;namespace=self.database;config={'hosts':[(self.host,self.port)]}
		if self.user and self.password:
			if len(self.user)>0:config['user']=self.user
			if len(self.password)>0:config['password']=self.password
		try:
			client=aerospike.client(config).connect();namespaces=client.info_all('namespaces');namespaces=[elem[1].strip()for elem in namespaces.values()]
			if namespace in namespaces:success=True
			else:self.error_msg_test_connection=f"Namespace '{namespace}' does not exist.";success=A
		except Exception as e:self.error_msg_test_connection=str(e);success=A
		finally:
			try:client.close()
			except:pass
		return success
	def get_available_tables(self):
		try:
			sets=set();client=self.connector;namespace=self.database;scan=client.scan(namespace,None)
			def callback(record):key,metadata,bins=record;sets.add(key[1])
			scan.foreach(callback);sets=list(sets);return sets
		except Exception as e:print(e);return[]
	def get_table_columns(self,table_name):
		try:
			bins=set();client=self.connector;set_name=table_name;namespace=self.database;scan=client.scan(namespace,set_name)
			def callback(record):
				_,_,record_bins=record
				for bin_name in record_bins.keys():bins.add(bin_name)
			scan.foreach(callback);bins=list(bins);return bins
		except Exception as e:return[]
	def get_data_table(self,table_name):
		client=self.connector;namespace=self.database;set_name=table_name;records=[];scan=client.scan(namespace,set_name)
		def callback(record):key,metadata,bins=record;records.append(bins)
		scan.foreach(callback);return sparta_8b01070954(pd.DataFrame(records))
	def get_data_table_query(self,sql,table_name=None):
		exec(sql,globals(),locals());filters_to_apply=eval('filters');client=self.connector;namespace=self.database;set_name=table_name;query=client.query(namespace,set_name)
		for(column,value)in filters_to_apply.items():
			if isinstance(value,tuple)and value[0]=='range':query.where(aerospike.predicates.between(column,value[1],value[2]))
			else:query.where(aerospike.predicates.equals(column,value))
		records=[]
		def callback(record):key,metadata,bins=record;records.append(bins);print(key)
		query.foreach(callback);return sparta_8b01070954(pd.DataFrame(records))
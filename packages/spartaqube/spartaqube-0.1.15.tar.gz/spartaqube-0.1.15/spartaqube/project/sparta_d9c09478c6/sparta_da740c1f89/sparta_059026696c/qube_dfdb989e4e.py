_A=None
import os,re,openpyxl,duckdb,pandas as pd
from project.sparta_d9c09478c6.sparta_da740c1f89.qube_b4d54ce7bf import EngineBuilder
class CsvConnector(EngineBuilder):
	def __init__(self,csv_path,csv_delimiter=_A):super().__init__(host=_A,port=_A);self.connector=self.build_csv(file_path=csv_path);self.is_csv=os.path.splitext(csv_path)[1].lower()=='.csv';self.csv_path=csv_path;self.csv_delimiter=csv_delimiter
	def test_connection(self):
		A=False
		try:
			if os.path.isfile(self.connector.file_path):return True
			else:self.error_msg_test_connection='Invalid file path';return A
		except Exception as e:print(f"Error: {e}");self.error_msg_test_connection=str(e);return A
	def get_available_tables(self):
		if self.is_csv:return self.get_available_tables_csv()
		else:return self.get_available_tables_xls()
	def get_available_tables_csv(self):return['sheet1']
	def get_available_tables_xls(self):
		try:workbook=openpyxl.load_workbook(self.csv_path);sheet_names=workbook.sheetnames;return sorted(sheet_names)
		except Exception as e:print('Exception get available tables metadata');print(e);self.error_msg_test_connection=str(e);return[]
	def get_data_table(self,table_name):
		if self.is_csv:return self.get_data_table_csv()
		else:return self.get_data_table_xls(table_name)
	def get_data_table_query(self,sql,table_name):
		def extract_table_name(sql_query):
			match=re.search('FROM\\s+(\\w+)',sql_query,re.IGNORECASE)
			if match:return match.group(1)
		sheet_name=extract_table_name(sql);globals()[sheet_name]=self.get_data_table(sheet_name);return duckdb.query(sql).df()
	def get_data_table_csv(self):
		if self.csv_delimiter is not _A:return pd.read_csv(self.csv_path,sep=self.csv_delimiter)
		else:return pd.read_csv(self.csv_path)
	def get_data_table_xls(self,table_name):return pd.read_excel(self.csv_path,sheet_name=table_name)
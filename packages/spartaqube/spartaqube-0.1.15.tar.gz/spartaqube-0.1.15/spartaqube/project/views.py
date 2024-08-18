import os,json,base64,json
def sparta_bdd41e1710():A=os.path.dirname(__file__);B=os.path.dirname(A);return json.loads(open(B+'/platform.json').read())['PLATFORM']
def sparta_b86411087f(b):return base64.b64decode(b).decode('utf-8')
def sparta_e009debfa7(s):return base64.b64encode(s.encode('utf-8'))
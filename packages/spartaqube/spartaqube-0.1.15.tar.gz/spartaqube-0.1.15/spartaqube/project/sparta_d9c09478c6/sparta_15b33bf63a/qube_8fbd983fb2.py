_A='utf-8'
import hmac,hashlib,base64,argparse
SMTP_REGIONS=['us-east-2','us-east-1','us-west-2','ap-south-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ap-northeast-1','ca-central-1','eu-central-1','eu-west-1','eu-west-2','sa-east-1','us-gov-west-1']
DATE='11111111'
SERVICE='ses'
MESSAGE='SendRawEmail'
TERMINAL='aws4_request'
VERSION=4
def sparta_9363eea300(key,msg):return hmac.new(key,msg.encode(_A),hashlib.sha256).digest()
def sparta_983cccb89a(secret_access_key,region):
	B=region
	if B not in SMTP_REGIONS:raise ValueError(f"The {B} Region doesn't have an SMTP endpoint.")
	A=sparta_9363eea300(('AWS4'+secret_access_key).encode(_A),DATE);A=sparta_9363eea300(A,B);A=sparta_9363eea300(A,SERVICE);A=sparta_9363eea300(A,TERMINAL);A=sparta_9363eea300(A,MESSAGE);C=bytes([VERSION])+A;D=base64.b64encode(C);return D.decode(_A)
def sparta_d67bdd7cdc():A=argparse.ArgumentParser(description='Convert a Secret Access Key for an IAM user to an SMTP password.');A.add_argument('secret',help='The Secret Access Key to convert.');A.add_argument('region',help='The AWS Region where the SMTP password will be used.',choices=SMTP_REGIONS);B=A.parse_args();print(sparta_983cccb89a(B.secret,B.region))
if __name__=='__main__':sparta_d67bdd7cdc()
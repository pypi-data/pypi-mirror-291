_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_d2cbd86ff0():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5463b48926(objectToCrypt):A=objectToCrypt;C=sparta_d2cbd86ff0();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_dfbcc8797c(apiAuth):A=apiAuth;B=sparta_d2cbd86ff0();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2dd47e5364(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_9ae0395e5f(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_2dd47e5364(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_7fea05618f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_2dd47e5364(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_fef132bd9b(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_7310808a24(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_fef132bd9b(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_332bbedf96(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_fef132bd9b(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_eed9bf0508(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_6c8da3fd31(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_eed9bf0508(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9b8ddf719d(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_eed9bf0508(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
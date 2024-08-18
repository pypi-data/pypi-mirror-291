_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_94e6cff18b():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_d3183a174e(objectToCrypt):A=objectToCrypt;C=sparta_94e6cff18b();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_044cbc8ab4(apiAuth):A=apiAuth;B=sparta_94e6cff18b();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_b0990e01e0(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_5ed7c7d1e1(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_b0990e01e0(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_f342665d06(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_b0990e01e0(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_912abdaf04(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_b0c6022d82(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_912abdaf04(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_0e81e60378(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_912abdaf04(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_c4ad62225e(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e118727ba9(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_c4ad62225e(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_4ce2f0ce8f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_c4ad62225e(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
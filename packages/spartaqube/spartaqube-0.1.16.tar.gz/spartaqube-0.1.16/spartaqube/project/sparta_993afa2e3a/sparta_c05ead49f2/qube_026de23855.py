_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_fb7deb4869():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_fb1e84e590(objectToCrypt):A=objectToCrypt;C=sparta_fb7deb4869();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_75e1c69ef8(apiAuth):A=apiAuth;B=sparta_fb7deb4869();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_5ceb59d950(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_c6f09eed60(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_5ceb59d950(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_e08fdf029b(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_5ceb59d950(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_32fda331a8(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_1e28a08a96(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_32fda331a8(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_4eb1f0b397(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_32fda331a8(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_d42a7a7821(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_54b18975cd(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_d42a7a7821(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a7f860dcac(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_d42a7a7821(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
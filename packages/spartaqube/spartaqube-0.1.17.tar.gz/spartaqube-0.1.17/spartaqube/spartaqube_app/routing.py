import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_addce897a6.sparta_c6f986b3b5 import qube_d8a7a34499,qube_b334bcb5eb
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_6b3e44380b(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/notebookWS',sparta_6b3e44380b(qube_d8a7a34499.NotebookWS)),url('ws/wssConnectorWS',sparta_6b3e44380b(qube_b334bcb5eb.WssConnectorWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)
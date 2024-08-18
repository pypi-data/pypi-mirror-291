import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_06ab2796ce.sparta_4973ea70c3 import qube_f63251c320,qube_84c762fee7
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
print('CHANNELS VERSION')
print(channels_ver)
def sparta_c318d66e7a(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/notebookWS',sparta_c318d66e7a(qube_f63251c320.NotebookWS)),url('ws/wssConnectorWS',sparta_c318d66e7a(qube_84c762fee7.WssConnectorWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)
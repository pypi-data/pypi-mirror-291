from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_b59b8fcd05.sparta_b12ee59733.qube_1e775e5950.sparta_80f1e45f70'
handler500='project.sparta_b59b8fcd05.sparta_b12ee59733.qube_1e775e5950.sparta_3dbd76e4fd'
handler403='project.sparta_b59b8fcd05.sparta_b12ee59733.qube_1e775e5950.sparta_e8f7667ad7'
handler400='project.sparta_b59b8fcd05.sparta_b12ee59733.qube_1e775e5950.sparta_6e832bf041'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]
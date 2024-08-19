from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_908ac57722.sparta_e76676a2c0.qube_6c8351943d.sparta_7615c43e9b'
handler500='project.sparta_908ac57722.sparta_e76676a2c0.qube_6c8351943d.sparta_82693370ea'
handler403='project.sparta_908ac57722.sparta_e76676a2c0.qube_6c8351943d.sparta_24381a759a'
handler400='project.sparta_908ac57722.sparta_e76676a2c0.qube_6c8351943d.sparta_e10859c995'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]
from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_582d4dfd84.sparta_e30c4ad1a4.qube_fb40ded8d3.sparta_2c021d8b72'
handler500='project.sparta_582d4dfd84.sparta_e30c4ad1a4.qube_fb40ded8d3.sparta_6b66729dc3'
handler403='project.sparta_582d4dfd84.sparta_e30c4ad1a4.qube_fb40ded8d3.sparta_242f181ec4'
handler400='project.sparta_582d4dfd84.sparta_e30c4ad1a4.qube_fb40ded8d3.sparta_6d0d9460e8'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]
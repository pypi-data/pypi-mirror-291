import os,django
from channels.routing import get_default_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','spartaqube_app.settings')
django.setup()
application=get_default_application()
"""Django's command-line utility for administrative tasks."""
import os
import sys


def sparta_d67bdd7cdc():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
            ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    sparta_d67bdd7cdc()

#END OF QUBE

import os
import sys
from django.core.wsgi import get_wsgi_application

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pacfreecongress.settings")

application = get_wsgi_application()

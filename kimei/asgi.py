import os
from django.core.asgi import get_asgi_application
from gmao import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kimei.settings')
application = get_asgi_application()

# Use routing.application or whatever is needed from routing

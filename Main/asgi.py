"""
ASGI config for Main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.asgi import get_asgi_application
from Home import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

application = get_asgi_application()

ws_urlpatterns = [
    #we denoted websocket path with "ws"
    path('ws/pizza/<order_id>',consumers.OrderProgress.as_asgi()) #order_id is dynamic id which we are getting from script tag declared in order.html and OrderProgress(view or classname) will be called 
]




application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(URLRouter(ws_urlpatterns))
})
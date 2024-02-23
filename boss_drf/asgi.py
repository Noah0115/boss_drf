"""
ASGI config for boss_drf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from back import routings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss_drf.settings')
application = ProtocolTypeRouter({
    'http': get_asgi_application(),     # 支持http请求
    'websocket': URLRouter(routings.websocket_urlpatterns),      # 支持websocket请求
})

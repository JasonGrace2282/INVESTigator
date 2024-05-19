from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/video/<path>", consumers.LicenseConsumer.as_asgi()),
]

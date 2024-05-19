from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings

from .license import read_frame as prediction


class LicenseConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        path = str(settings.MEDIA_ROOT / self.scope["url_route"]["kwargs"]["path"])
        self.prediction(path)

    def prediction(self, path: str):
        print(f"Finding prediction for {path}")
        for txt, time, p in prediction(path):
            self.send_json({
                "license": txt,
                "timestamp": round(time, 2),
                "p": round(p, 2)
            })

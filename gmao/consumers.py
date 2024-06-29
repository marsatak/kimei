from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import models


class YourConsumerClass(AsyncWebsocketConsumer):
    async def connect(self):
        # Import models here when needed
        from .models import Doleance, Personnel
        # Rest of your consumer logic

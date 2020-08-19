import asyncio
import json

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Ticket

class TicketConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept"
        })
        await self.channel_layer.group_add("gossip", self.channel_name)
        print (f'Added {self.channel_name} channel to gossip')

    async def websocket_receive(self, event):
        print ("receive", event)

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print (f'Removed {self.channel_name} channel to gossip')

    async def ticket_gossip(self, event):
        print (event)
        event_string = json.dumps(event)
        await self.send({
            "type": "websocket.send",
            "text": event_string
            })
        print (f'Got message {event} at {self.channel_name}')
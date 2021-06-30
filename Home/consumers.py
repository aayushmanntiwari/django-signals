import json
import redis
import channels
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from django.utils import text
from Orders.models import Orders

#This class will be called via ws url parttern(just like we did in urls.py) which we included in asgi.py
#This consist of three method conenct ,receive and disconnect 
#when we want to send data from backend to frontend use connect
#when data is coming from front-end to backend use receive
class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order-{}'.format(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name)
        orders = Orders.give_order_details(self.room_name)
        self.accept()
        self.send(text_data=json.dumps({
            'payload': orders
        }))
        print("#######CONNECTED############")
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("DISCONNECED CODE: ",code)

    #when change in model field this method will be called 
    def order_status(self,event):
        data = json.loads(event['text'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'payload': data
        }))
    
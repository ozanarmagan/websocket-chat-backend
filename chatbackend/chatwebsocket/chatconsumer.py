import asyncio
import json
from channels.consumer import AsyncConsumer
from .models import *
from asgiref.sync import sync_to_async

@sync_to_async
def get_users():
    return list(
        User.objects.all()
    )

@sync_to_async
def create_user(name,channel):
    newuser = User.objects.create(name=name,channel=channel)


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print('connected',event)
        chat_room = "chatroom"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })
    
    async def websocket_receive(self,event):
        message = json.loads(event.get('text',None))
        if message["type"] == "getUsers":
            users=[]
            userlist = await get_users()
            for user in userlist:
                users.append(user.name)
            toSend = {"type":"online_users","content":str(users)}
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"online_users",
                    "text":str(toSend),
                    "sender":self.channel_name
                }
            )
        elif message["type"] == "add_user":
            await create_user(message["content"],self.channel_name)
            users=[]
            userlist = await get_users()
            for user in userlist:
                users.append(user.name)
            toSend = {"type":"online_users","content":str(users)}
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"online_users",
                    "text":str(toSend),
                    "sender":self.channel_name
                }
            )
        elif message["type"] == "new_message":
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"new_essage",
                    "text": message["message"],
                    "user": User.objects.get(channel=self.channel_name).name,
                    "sender":self.channel_name
                }
            )
    async def online_users(self,event):
        text = {"message_type":"online_users","users":str(event['text'])}
        await self.send({
            "type":"websocket.send",
            "text": str(text),
        })
    async def new_message(self,event):
        if self.channel_name != event['sender']:
            await self.send_json({
                "type":"websocket.send",
                "message_type":event["type"],
                "message": event["text"],
                "user": event["user"]
            })
    


        



            


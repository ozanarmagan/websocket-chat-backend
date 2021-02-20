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

@sync_to_async
def remove_user(channel):
    User.objects.filter(channel=channel).delete()

@sync_to_async
def get_username(channel):
    return User.objects.get(channel=channel).name


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
        if message["type"] == "get_users":
            users=[]
            userlist = await get_users()
            for user in userlist:
                users.append(user.name)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"online_users",
                    "text": users,
                    "sender": self.channel_name
                }
            )
        elif message["type"] == "add_user":
            await create_user(message["content"],self.channel_name)
            users=[]
            userlist = await get_users()
            for user in userlist:
                users.append(user.name)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"online_users",
                    "text": users,
                    "sender":self.channel_name
                }
            )
        elif message["type"] == "new_message":
            username = await get_username(self.channel_name)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"new_message",
                    "text": message["message"],
                    "user": username,
                    "sender": self.channel_name
                }
            )
    async def online_users(self,event):
        text = {"message_type":"online_users","users":event["text"]}
        await self.send({
            "type":"websocket.send",
            "text": str(text)
        })
    async def new_message(self,event):
        text = {"message_type":"new_message","message":event["text"],"user":event["user"]}
        await self.send({
            "type":"websocket.send",
            "text": str(text)
            })
    async def websocket_disconnect(self,user):
        await remove_user(self.channel_name)
        users=[]
        userlist = await get_users()
        for user in userlist:
            users.append(user.name)
            await self.channel_layer.group_send(
            self.chat_room,
            {
                "type":"online_users",
                "text": users,
                "sender": self.channel_name
            }
        )

    


        



            


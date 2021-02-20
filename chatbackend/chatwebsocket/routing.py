from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.conf.urls import url
from channels.security.websocket import AllowedHostsOriginValidator
from .chatconsumer import *

application = ProtocolTypeRouter({
  'websocket': AllowedHostsOriginValidator(
    URLRouter(
      [
        url("", ChatConsumer.as_asgi())
      ]
    )
  )
})
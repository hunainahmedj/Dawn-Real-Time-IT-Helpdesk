from django.urls import path

from .consumers import TicketConsumer

websocket_urlpatterns = [
    path('notifications/ticket', TicketConsumer),
]
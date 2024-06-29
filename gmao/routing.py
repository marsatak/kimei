from django.urls import path
from django.utils.module_loading import import_string


# Use a function to lazily import the consumer
def get_consumer():
    return import_string('gmao.consumers.YourConsumerClass')


websocket_urlpatterns = [
    path('ws/some_path/', get_consumer()),
    # Add other WebSocket routes as needed
]

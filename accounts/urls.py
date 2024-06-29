from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    # MIRE DE BIENVENUE
    path('', views.index, name='index'),
]

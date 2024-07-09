from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    # MIRE DE BIENVENUE
    path('', views.login_view, name='login-admin'),
    path('accounts/login/', views.login_view, name='login-admin'),
    path('accounts/logout/', views.logout_view, name='logout-admin'),
    path('accounts/login/change-password/', views.change_password, name='change_password'),

]

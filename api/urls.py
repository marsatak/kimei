from django.urls import path
from api.api_views import LoginView, LogoutView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.api_views import TechnicienViewSet, get_csrf_token
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r'technicien', TechnicienViewSet, basename='technicien')

urlpatterns = [
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-info/', UserInfoView.as_view(), name='user_info'),
    path('api/', include(router.urls)),
]

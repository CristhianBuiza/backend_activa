from django.urls import path
from .views import RelationView , RegisterView,LoginView,UserView,ProfileUpdateView, UpdateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UpdateView.as_view(), name='update'),
    path('update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('relation/', RelationView.as_view(), name='relation'),
    path('user/', UserView.as_view(), name='user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist')
]
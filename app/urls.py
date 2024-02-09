from django.contrib import admin
from django.urls import path, include

from .views import home_view, login_view, logout_view, find_user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('clasify/', find_user_view, name='classify'),
    path('api/', include('profiles.urls'))
]

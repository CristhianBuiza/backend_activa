from django.urls import path
from .views import HelpView

urlpatterns = [
    path('help/', HelpView.as_view(), name="help"),
]
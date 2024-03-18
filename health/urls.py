from django.urls import path
from .views import HealthDetailView, HealthView

urlpatterns = [
    path('healths/', HealthView.as_view(), name="reminder-list"),
    path('healths/<int:pk>', HealthDetailView.as_view(), name='reminder-detail')
]
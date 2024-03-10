from django.urls import path
from .views import ServicesView,ServiceView, TagView

urlpatterns = [
    path('service/', ServicesView.as_view(), name="service-list"),
    path('service/<int:pk>', ServiceView.as_view(), name='service-detail'),
    path("service/tags", TagView.as_view(), name="service-tag-list")
]
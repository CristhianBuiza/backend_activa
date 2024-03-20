from django.urls import path
from .views import ServicesView,ServiceView, TagView, TaxiServiceDetailView, TaxiServiceView

urlpatterns = [
    path('service/', ServicesView.as_view(), name="service-list"),
    path('service/<int:pk>', ServiceView.as_view(), name='service-detail'),
    path("service/tags", TagView.as_view(), name="service-tag-list"),
    path('service/taxi', TaxiServiceView.as_view(), name='taxi-service-list'),
    path('service/taxi/<int:pk>', TaxiServiceDetailView.as_view(), name='taxi-service-detail')
]
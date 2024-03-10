from django.urls import path
from .views import CommunityView,CommunityDetailView, TagCommunityView

urlpatterns = [
    path('community/', CommunityView.as_view(), name="reminder-list"),
    path('community/<int:pk>', CommunityDetailView.as_view(), name='reminder-detail'),
    path('community/tags', TagCommunityView.as_view(), name="reminder-tag-list"),
]
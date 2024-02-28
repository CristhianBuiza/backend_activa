from django.urls import path
from .views import ReminderView, ReminderDetailView

urlpatterns = [
    path('reminders/', ReminderView.as_view(), name="reminder-list"),
    path('reminders/<int:pk>', ReminderDetailView.as_view(), name='reminder-detail')
]
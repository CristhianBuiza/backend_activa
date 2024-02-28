from django.shortcuts import render
from .models import Reminder
from .serializers import ReminderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from app.helpers.get_user_by_token import get_user_by_token

# Create your views here.
class ReminderView(APIView):
    def get(self, request):  
        user = get_user_by_token(request)
        reminders = Reminder.objects.filter(user=user)
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        # create a new reminder
        user = get_user_by_token(request)
        data = request.data
        data['user'] = user.id
        serializer = ReminderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

        

    def put(self, request, pk):
        # Update a reminder
        user = get_user_by_token(request)
        data = request.data
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        if reminder.user != user:
            raise AuthenticationFailed('Unauthenticated')
        serializer = ReminderSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            reminder = serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        # Get object with this pk
        
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        reminder.delete()
        return Response({
            "message": "Reminder with id `{}` has been deleted.".format(pk)
        }, status=204)
        
class ReminderDetailView(APIView):
    def get(self, request, pk):
        # get reminder by id
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data)
        
    def put(self, request, pk):
        # Update a reminder
        data = request.data
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        serializer = ReminderSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            reminder = serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        # Get object with this pk
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        reminder.delete()
        return Response({
            "message": "Reminder with id `{}` has been deleted.".format(pk)
        }, status=204)
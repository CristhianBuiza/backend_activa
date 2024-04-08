from django.shortcuts import render

from rest_framework.response import Response
from .models import Reminder
from .serializers import ReminderSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from app.helpers.get_user_by_token import get_user_by_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from app.helpers.normalize_response import NormalizeResponse

# Create your views here.

class ReminderView(APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    @swagger_auto_schema(responses={200: ReminderSerializer(many=True)})
    def get(self, request):  
        day = request.query_params.get('day', None)
        order_date = request.query_params.get('order', None)
        user = request.user
        if day:
            reminders = Reminder.objects.filter(user=user, day=day).order_by('hour_start')
        if order_date == 'asc':
            reminders = Reminder.objects.filter(user=user).order_by('day', 'hour_start')
        elif order_date == 'desc':
            reminders = Reminder.objects.filter(user=user).order_by('-day', '-hour_start')
        else:
            reminders = Reminder.objects.filter(user=user).order_by('day', 'hour_start')
        serializer = ReminderSerializer(reminders, many=True)

        return Response({
                "status": status.HTTP_200_OK,
                "message": "Recordatorios obtenidos correctamente",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(request_body=ReminderSerializer, responses={200: ReminderSerializer})
    def post(self, request):
        # create a new reminder
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = ReminderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return NormalizeResponse(
            data=serializer.data,
            message="Recordatorio creado correctamente",
            status=status.HTTP_201_CREATED
            )
        else:
            return NormalizeResponse(serializer.errors, status.HTTP_400_BAD_REQUEST, "Error en la creación del recordatorio")

        
    @swagger_auto_schema(request_body=ReminderSerializer(partial=True), responses={200: ReminderSerializer})
    def put(self, request, pk):
        # Update a reminder
        user = request.user
        data = request.data
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        if reminder.user != user:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no tiene reminders"
            )
        serializer = ReminderSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            reminder = serializer.save()
        return NormalizeResponse(
            data=serializer.data,
            message="Recordatorio actualizado correctamente",
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={204: 'Reminder deleted successfully', 404: 'Reminder not found'})
    def delete(self, request, pk):
        # Get object with this pk
        
        reminder = get_object_or_404(Reminder.objects.all(), pk=pk)
        reminder.delete()
        return NormalizeResponse(
            status= status.HTTP_204_NO_CONTENT,
            message= "Recordatorio con el id `{}` ha sido eliminado".format(pk)
            )

class ReminderDetailView(APIView):
    def get(self, request, pk):
        user = request.user
        my_reminder = Reminder.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Recordatorio no encontrado"
            )
        serializer = ReminderSerializer(reminder)
        return NormalizeResponse(
            data=serializer.data,
            message="Recordatorio obtenido correctamente",
            status=status.HTTP_200_OK
        )
        
    def put(self, request, pk):
        user = request.user
        my_reminder = Reminder.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Recordatorio no encontrado"
            )
        data = request.data
        serializer = ReminderSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid():
            reminder = serializer.save()
        else:
            return NormalizeResponse(serializer.errors, status.HTTP_400_BAD_REQUEST, "Error en la actualización del recordatorio")
        return NormalizeResponse(
            data=serializer.data,
            message="Recordatorio actualizado correctamente",
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        # Get object with this pk
        user = request.user
        my_reminder = Reminder.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Recordatorio no encontrado"
            )
        reminder.delete()
        return NormalizeResponse(
            status= status.HTTP_204_NO_CONTENT,
            message= "Recordatorio con el id `{}` ha sido eliminado".format(pk)
            )
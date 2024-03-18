from django.shortcuts import render
from .models import Health
from .serializers import HealthSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from app.helpers.get_user_by_token import get_user_by_token
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.helpers.normalize_response import NormalizeResponse
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class HealthView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    @swagger_auto_schema(responses={200: HealthSerializer(many=True)})
    def get(self, request):  
        day = request.query_params.get('day', None)
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed as e:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        if day:
            reminders = Health.objects.filter(user=user, day=day)
        else:
            reminders = Health.objects.filter(user=user).order_by('day')
        serializer = HealthSerializer(reminders, many=True)
        return NormalizeResponse (
            data=serializer.data,
            message="Reminders obtenidos correctamente",
            status=status.HTTP_200_OK
        )
        
    @swagger_auto_schema(request_body=HealthSerializer, responses={200: HealthSerializer})
    def post(self, request):
        # create a new reminder
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        data = request.data
        data['user'] = user.id
        serializer = HealthSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return NormalizeResponse(
            data=serializer.data,
            message="Recordatorio creado correctamente",
            status=status.HTTP_201_CREATED
            )
        else:
            return NormalizeResponse(serializer.errors, status.HTTP_400_BAD_REQUEST, "Error en la creación del recordatorio")
        
    @swagger_auto_schema(request_body=HealthSerializer(partial=True), responses={200: HealthSerializer})
    def put(self, request, pk):
        # Update a reminder
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        data = request.data
        reminder = get_object_or_404(Health.objects.all(), pk=pk)
        if reminder.user != user:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no tiene reminders"
            )
        serializer = HealthSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            reminder = serializer.save()
        return NormalizeResponse(
            data=serializer.data,
            message="Archivo actualizado correctamente",
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={204: 'Reminder deleted successfully', 404: 'Reminder not found'})
    def delete(self, request, pk):
        # Get object with this pk
        
        reminder = get_object_or_404(Health.objects.all(), pk=pk)
        reminder.delete()
        return NormalizeResponse(
            status= status.HTTP_204_NO_CONTENT,
            message= "Archivo con el id `{}` ha sido eliminado".format(pk)
            )

class HealthDetailView(APIView):
    def get(self, request, pk):
        try :
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        my_reminder = Health.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Recordatorio no encontrado"
            )
        serializer = HealthSerializer(reminder)
        return NormalizeResponse(
            data=serializer.data,
            message="Archivo obtenido correctamente",
            status=status.HTTP_200_OK
        )
        
    def put(self, request, pk):
        # Update a reminder
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        my_reminder = Health.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Recordatorio no encontrado"
            )
        data = request.data
        serializer = HealthSerializer(instance=reminder, data=data, partial=True)
        if serializer.is_valid():
            reminder = serializer.save()
        else:
            return NormalizeResponse(serializer.errors, status.HTTP_400_BAD_REQUEST, "Error en la actualización del recordatorio")
        return NormalizeResponse(
            data=serializer.data,
            message="Archivo actualizado correctamente",
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        # Get object with this pk
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        my_reminder = Health.objects.filter(user=user, id=pk)
        try:
            reminder = get_object_or_404(my_reminder, pk=pk)
        except:
            return NormalizeResponse(
            status= status.HTTP_404_NOT_FOUND,
            message= "Archivo no encontrado"
            )
        reminder.delete()
        return NormalizeResponse(
            status= status.HTTP_204_NO_CONTENT,
            message= "Archivo con el id `{}` ha sido eliminado".format(pk)
            )
       
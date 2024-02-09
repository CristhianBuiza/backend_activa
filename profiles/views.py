from django.shortcuts import render
from .models import Profile
from .serializers import ProfileSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework import status
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {
                    "status": "400",
                    "message":"Error en el registro",
                    "errors":serializer.errors
                }
                , status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('Invalid username')
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')
        
        payload = {
            "id":user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie('jwt', token, httponly=True)
        response.data = {'token':token}
        return response
    
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
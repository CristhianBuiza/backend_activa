import jwt, datetime
import base64
from app.utils import classify_face

from django.core.files.base import ContentFile 
from .models import Profile
from logs.models import Log
from .serializers import UserSerializer,UserRecognitionSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth.models import User
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from app.helpers.normalize_response import NormalizeResponse
# Create your views here.
class RegisterView(APIView):
    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            user = User.objects.get(username=user_data['username'])
            payload = {
                "id": user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response_data = serializer.data
            response_data['token'] = token
            response = NormalizeResponse(response_data, status.HTTP_201_CREATED, "Usuario creado correctamente")
            response.set_cookie('jwt', token, httponly=True)
            return response
        else:
            return NormalizeResponse(serializer.errors, status.HTTP_401_UNAUTHORIZED, "Error en el registro")

class LoginView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'image_base64': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ), responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )})
    def post(self, request):
        # Get authentication with cookies
        if 'jwt' in request.COOKIES:
            try:
                token = request.COOKIES.get('jwt')
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user_id = payload['id']
                user = User.objects.filter(id=user_id).first()
                profile = Profile.objects.get(user=user)
                if user:
                    # Devolver datos del usuario si la sesión está activa
                    return NormalizeResponse(
                        data={
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'role': profile.role
                        },
                        message="Usuario autenticado correctamente",
                        status=status.HTTP_200_OK,
                    )
            except jwt.ExpiredSignatureError:
                return NormalizeResponse(
                    status= status.HTTP_401_UNAUTHORIZED,
                    message= "Usuario no autenticado"
                )
            except jwt.InvalidTokenError:
                return NormalizeResponse(
                    status= status.HTTP_401_UNAUTHORIZED,
                    message= "Usuario no autenticado"
                )
                
        username=request.data.get('username')
        password=request.data.get('password')
        user = User.objects.filter(username=username).first()
        profile = Profile.objects.get(user=user)
        image_base64=request.data.get('image_base64')
        if user is None:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no encontrado"
            )
        
        if image_base64:
            x = Log()
            _, str_img = image_base64.split(';base64,')
            decoded_file = base64.b64decode(str_img)
            x.photo = ContentFile(decoded_file, name='upload.jpg')
            x.save()
            res = classify_face(x.photo.path, user.username)
            if res == user.username:
                pass
            else:
                return NormalizeResponse(
                status= status.HTTP_401_UNAUTHORIZED,
                message= "Face recognition failed"
                )
        if user.check_password(password):
            pass
        else:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Password invalid"
            )

        payload = {
            "id":user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
       
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = NormalizeResponse({'token': token, 'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, "role": profile.role}, status.HTTP_200_OK, "success")
        response.set_cookie('jwt', token, httponly=True)
        return response
    
class UserView(APIView):
    @swagger_auto_schema(
        responses={
            200: UserSerializer,  # Successful response returns user data
            401: 'Unauthenticated'  # Possible unauthenticated response
        }
    )
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return NormalizeResponse(
            data=serializer.data,
            message="Usuario obtenido correctamente",
            status=status.HTTP_200_OK
        ) 
    
class ProfileUpdateView(APIView):
    @swagger_auto_schema(
        request_body=UserRecognitionSerializer(partial=True),  # Indicate that partial updates are allowed
        responses={
            200: UserRecognitionSerializer,  # Successful response with the updated profile data
            400: 'Bad Request - Invalid Data',  # Data validation error
            401: 'Unauthenticated - Invalid or expired JWT token'  # Authentication failure
        }
    )
    def patch(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return NormalizeResponse(
            status= status.HTTP_401_UNAUTHORIZED,
            message= "Usuario no autenticado"
            )

        user = User.objects.filter(id=payload['id']).first()
        profile = Profile.objects.get(user=user)
        serializer = UserRecognitionSerializer(profile, data=request.data, partial=True) # partial=True permite la actualización parcial
        if serializer.is_valid():
            serializer.save()
            return NormalizeResponse(
                data=serializer.data,
                message="Perfil actualizado correctamente",
                status=status.HTTP_200_OK
            )
        else:
            return NormalizeResponse(
                status= status.HTTP_400_BAD_REQUEST,
                message= "Error en la actualización del perfil"

            )
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status


def get_user_by_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Token doesnt provided",
                }, status=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Token doesnt provided",
                }, status=status.HTTP_401_UNAUTHORIZED)
    return User.objects.get(id=payload['id'])
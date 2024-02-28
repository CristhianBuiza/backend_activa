import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

def get_user_by_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('No user token found')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    return User.objects.get(id=payload['id'])
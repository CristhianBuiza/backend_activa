from app.helpers.get_user_by_token import get_user_by_token
from drf_yasg.utils import swagger_auto_schema
from help.serializer import HelpSerializer
from rest_framework import permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .models import Help
from app.helpers.normalize_response import NormalizeResponse

# Create your views here.
class HelpView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=HelpSerializer, responses={200: HelpSerializer})
    def post(self, request):
        user = request.user
        screen = request.data.get('screen')
        print(user)
        if not screen:
            return NormalizeResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="El campo screen es requerido"
            )
        help = Help.objects.create(
            screen=screen,
            user=user
        )
        serializer = HelpSerializer(help)
        return NormalizeResponse(
            data=serializer.data,
            message="Solicitud de ayuda enviada correctamente"
        )

from app.helpers.get_user_by_token import get_user_by_token
from help.serializer import HelpSerializer
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .models import Help
from app.helpers.normalize_response import NormalizeResponse

# Create your views here.
class HelpView(APIView):
    def post(self, request):
        scream = request.data.get('scream')
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed :
            return NormalizeResponse(
            status= status.HTTP_400_BAD_REQUEST,
            message= "Usuario no autenticado"
            )
        if not scream:
            return NormalizeResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message="El campo scream es requerido"
            )
        help = Help.objects.create(
            scream=scream,
            user=user
        )
        serializer = HelpSerializer(help)
        return NormalizeResponse(
            data=serializer.data,
            message="Solicitud de ayuda enviada correctamente"
        )

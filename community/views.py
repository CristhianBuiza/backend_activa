from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CommunitySerializer, TagCommunitySerializer
from app.helpers.normalize_response import NormalizeResponse
from .models import Community, TagCommunity
# Create your views here.
class CommunityView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las comunidades o comunidades filtradas por tag",
        responses={
            200: CommunitySerializer(many=True),
            404: 'No se encontraron comunidades'
        },
        manual_parameters=[
            openapi.Parameter(
                'tag', openapi.IN_QUERY,
                description="Filtrar comunidades por el nombre del tag",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        tag = request.GET.get('tag')
        if tag:
            tag = TagCommunity.objects.filter(name=tag).first()
            if not tag:
                return NormalizeResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    message="No se encontró el tag"
                )
            community = Community.objects.filter(tag=tag)
        else:
            community = Community.objects.all()
        serializer = CommunitySerializer(community, many=True)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron comunidades"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Comunidades obtenidas correctamente"
        )
        
class CommunityDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene los detalles de una comunidad específica por su ID",
        responses={
            200: CommunitySerializer(),
            404: 'No se encontró la comunidad'
        }
    )
    def get(self, request, pk):
        community = Community.objects.filter(pk=pk).first()
        if not community:
            return NormalizeResponse(
                status=404,
                message="No se encontró la comunidad"
            )
        serializer = CommunitySerializer(community)
        return NormalizeResponse(
            data=serializer.data,
            message="Comunidad obtenida correctamente"
        )
class TagCommunityView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los tags",
        responses={200: TagCommunitySerializer(many=True), 404: 'No se encontraron tags'}
    )
    def get(self, request):
        tags = TagCommunity.objects.all()
        serializer = TagCommunitySerializer(tags, many=True)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron tags"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Tags obtenidos correctamente"
        )
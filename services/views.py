from drf_yasg import openapi
from rest_framework.views import APIView
from app.helpers.normalize_response import NormalizeResponse
from .models import Service, TagService
from .serializers import ServiceSerializer, TagSerializer
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class ServicesView(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los servicios o servicios filtrados por tag",
        responses={
            200: ServiceSerializer(many=True),
            404: 'No se encontraron servicios'
        },
        manual_parameters=[
            openapi.Parameter('tag', openapi.IN_QUERY, description="Filtrar servicios por tag", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        # get tag
        tag = request.GET.get('tag')
        if tag:
            tag = TagService.objects.filter(name=tag).first()
            if not tag:
                return NormalizeResponse(
                    status=404,
                    message="No se encontró el tag"
                )
            services = Service.objects.filter(tag=tag)
        else:
            services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron  servicios"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Servicios obtenidos correctamente"
        )

        
class ServiceView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene un servicio específico por su ID",
        responses={200: ServiceSerializer(), 404: 'No se encontró el servicio'}
    )
    def get(self, request, pk):
        service = Service.objects.filter(pk=pk).first()
        if not service:
            return NormalizeResponse(
                status=404,
                message="No se encontró el servicio"
            )
        serializer = ServiceSerializer(service)
        return NormalizeResponse(
            data=serializer.data,
            message="Servicio obtenido correctamente"
        )

class TagView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los tags",
        responses={200: TagSerializer(many=True), 404: 'No se encontraron tags'}
    )
    def get(self, request):
        tags = TagService.objects.all()
        serializer = TagSerializer(tags, many=True)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron tags"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Tags obtenidos correctamente"
        )
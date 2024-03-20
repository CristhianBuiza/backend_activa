from app.helpers.get_user_by_token import get_user_by_token
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from app.helpers.normalize_response import NormalizeResponse
from .models import AttentionTaxiService, Service, TagService, TaxiService
from .serializers import ServiceSerializer, TagSerializer, TaxiServiceDetailSerializer, TaxiServiceSerializer
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
        
class TaxiServiceView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los servicios de taxi por usuario",
        responses={200: ServiceSerializer(many=True), 404: 'No se encontraron servicios de taxi'}
    )
    def get(self, request):
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
                status=401,
                message="Usuario no autenticado"
            )
        taxis = TaxiService.objects.filter(user=user)
        serializer = TaxiServiceSerializer(taxis, many=True)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron servicios de taxi"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Servicio de taxi obtenido correctamente"
        )

class TaxiServiceDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene un servicio de taxi específico por su ID",
        responses={200: ServiceSerializer(), 404: 'No se encontró el servicio de taxi'}
    )
    def get(self, request, pk):
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
                status=401,
                message="Usuario no autenticado"
            )
        taxis = TaxiService.objects.filter(user=user, pk=pk).first()
        serializer = TaxiServiceDetailSerializer(taxis)
        if not serializer.data:
            return NormalizeResponse(
                status=404,
                message="No se encontraron servicios de taxi"
            )
        return NormalizeResponse(
            data=serializer.data,
            message="Servicios de taxi obtenidos correctamente"
        )

class TaxiReservation(APIView):
    @swagger_auto_schema(
        operation_description="Reserva un servicio de taxi",
        responses={200: 'Reserva realizada correctamente', 404: 'No se encontró el servicio de taxi'}
    )
    def post(self, request, pk):
        try:
            user = get_user_by_token(request)
        except AuthenticationFailed:
            return NormalizeResponse(
                status=401,
                message="Usuario no autenticado"
            )
        taxi = TaxiService.objects.filter(pk=pk).first()
        if not taxi:
            return NormalizeResponse(
                status=404,
                message="No se encontró el servicio de taxi"
            )
        if taxi.user == user:
            return NormalizeResponse(
                status=400,
                message="No puedes reservar tu propio servicio"
            )
        taxi_reservation = AttentionTaxiService.objects.create(user=user, taxi_service=taxi)
        return NormalizeResponse(
            data=taxi_reservation.id,
            message="Reserva realizada correctamente"
        )
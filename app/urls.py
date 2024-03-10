from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

schema_view = get_schema_view(
   openapi.Info(
      title="ACTIVA API",
      default_version='v1',
      description="Documentacion detallada de activa API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cbuiza@rpalatam.com.pe"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   # permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url='/admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include('profiles.urls')),
    path('api/', include('reminders.urls')),
    path('api/', include('services.urls')),
    path('api/', include('community.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

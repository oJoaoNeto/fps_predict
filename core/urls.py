"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from hardware.views import HardwareComponentViewSet, PCBuildViewSet, OptimizeBuildView
from prediction.views import FpsPredictionViewSet, PredictFpsView

# Definindo o router do REST Framework
router = DefaultRouter()
router.register(r'components', HardwareComponentViewSet, basename='component')
router.register(r'builds', PCBuildViewSet, basename='build')
router.register(r'predictions', FpsPredictionViewSet, basename='prediction')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints do Router
    path('api/', include(router.urls)),
    
    # Endpoints Customizados
    path('api/predict-fps/', PredictFpsView.as_view(), name='predict-fps'),
    path('api/optimize-build/', OptimizeBuildView.as_view(), name='optimize-build'),
    
    # Documentacao OpenAPI/Swagger (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

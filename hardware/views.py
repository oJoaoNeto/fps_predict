from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from hardware.models import HardwareComponent, PCBuild
from hardware.serializers import (
    HardwareComponentSerializer, 
    PCBuildSerializer, 
    OptimizeBuildRequestSerializer
)
from hardware.optimizer import find_best_build, OptimizationError

class HardwareComponentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Listar e filtrar componentes de hardware ativos.
    Filtros suportados por Query Params:
    - category: CPU, GPU, RAM, MOBO, PSU, STORAGE
    - min_price: Preço mínimo
    - max_price: Preço máximo
    """
    queryset = HardwareComponent.objects.filter(is_active=True).order_by('id')
    serializer_class = HardwareComponentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category=category.upper())
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

class PCBuildViewSet(viewsets.ModelViewSet):
    """
    ViewSet para salvar e visualizar as builds criadas.
    """
    queryset = PCBuild.objects.all().order_by('-created_at')
    serializer_class = PCBuildSerializer

    def perform_create(self, serializer):
        cpu = serializer.validated_data['cpu']
        gpu = serializer.validated_data['gpu']
        ram = serializer.validated_data['ram']
        motherboard = serializer.validated_data['motherboard']
        psu = serializer.validated_data['psu']
        storage = serializer.validated_data['storage']
        
        total_cost = cpu.price + gpu.price + ram.price + motherboard.price + psu.price + storage.price
        user = self.request.user if self.request.user.is_authenticated else None
        
        serializer.save(total_cost=total_cost, user=user)

class OptimizeBuildView(APIView):
    """
    Recomenda a melhor configuração de PC para CS:GO que caiba no orçamento.
    """
    @extend_schema(
        request=OptimizeBuildRequestSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request, *args, **kwargs):
        serializer = OptimizeBuildRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data = serializer.validated_data
        try:
            build = find_best_build(
                budget=data['budget'],
                resolution=data['resolution'],
                quality_preset=data['quality_preset'],
                priority=data['priority']
            )
            
            response_data = {
                'cpu': HardwareComponentSerializer(build['cpu']).data,
                'gpu': HardwareComponentSerializer(build['gpu']).data,
                'motherboard': HardwareComponentSerializer(build['motherboard']).data,
                'ram': HardwareComponentSerializer(build['ram']).data,
                'psu': HardwareComponentSerializer(build['psu']).data,
                'storage': HardwareComponentSerializer(build['storage']).data,
                'total_cost': build['total_cost'],
                'fps_predicted': build['fps'],
                'budget_utilization_percent': build['budget_utilization_percent'],
                'priority_applied': data['priority'],
                'settings': {
                    'resolution': data['resolution'],
                    'quality_preset': data['quality_preset']
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
            
        except OptimizationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

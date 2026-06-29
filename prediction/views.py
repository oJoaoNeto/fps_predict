from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from games.models import Game
from hardware.models import HardwareComponent
from prediction.models import FpsPrediction
from prediction.serializers import (
    FpsPredictionSerializer, 
    PredictFpsRequestSerializer
)
from prediction.predictor import predict_fps

class FpsPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Visualizar histórico de previsões de FPS salvas.
    """
    queryset = FpsPrediction.objects.all().order_by('-created_at')
    serializer_class = FpsPredictionSerializer

class PredictFpsView(APIView):
    """
    Calcula e registra uma nova previsão de FPS para um jogo e configuração de hardware específicos.
    """
    @extend_schema(
        request=PredictFpsRequestSerializer,
        responses={201: FpsPredictionSerializer, 400: dict, 404: dict}
    )
    def post(self, request, *args, **kwargs):
        serializer = PredictFpsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        data = serializer.validated_data
        
        try:
            game = Game.objects.get(id=data['game_id'])
            cpu = HardwareComponent.objects.get(id=data['cpu_id'], category='CPU')
            gpu = HardwareComponent.objects.get(id=data['gpu_id'], category='GPU')
        except Game.DoesNotExist:
            return Response({'error': 'Jogo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except HardwareComponent.DoesNotExist:
            return Response({'error': 'CPU ou GPU inválida ou não cadastrada.'}, status=status.HTTP_404_NOT_FOUND)
            
        fps = predict_fps(
            game_name=game.name,
            cpu_specs=cpu.specs,
            gpu_specs=gpu.specs,
            ram_gb=data['ram_gb'],
            resolution=data['resolution'],
            quality_preset=data['quality_preset']
        )
        
        prediction = FpsPrediction.objects.create(
            game=game,
            cpu=cpu,
            gpu=gpu,
            ram_gb=data['ram_gb'],
            resolution=data['resolution'],
            quality_preset=data['quality_preset'],
            predicted_fps=fps
        )
        
        response_serializer = FpsPredictionSerializer(prediction)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

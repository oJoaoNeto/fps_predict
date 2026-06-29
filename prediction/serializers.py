from rest_framework import serializers
from prediction.models import FpsPrediction
from games.serializers import GameSerializer
from hardware.serializers import HardwareComponentSerializer

class FpsPredictionSerializer(serializers.ModelSerializer):
    game_details = GameSerializer(source='game', read_only=True)
    cpu_details = HardwareComponentSerializer(source='cpu', read_only=True)
    gpu_details = HardwareComponentSerializer(source='gpu', read_only=True)

    class Meta:
        model = FpsPrediction
        fields = [
            'id', 'game', 'cpu', 'gpu', 'ram_gb', 'resolution', 
            'quality_preset', 'predicted_fps', 'created_at',
            'game_details', 'cpu_details', 'gpu_details'
        ]
        read_only_fields = ['predicted_fps', 'created_at']

class PredictFpsRequestSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    cpu_id = serializers.IntegerField()
    gpu_id = serializers.IntegerField()
    ram_gb = serializers.IntegerField(min_value=4, max_value=128)
    resolution = serializers.ChoiceField(choices=['1080p', '1440p', '4K'])
    quality_preset = serializers.ChoiceField(choices=['Low', 'Medium', 'High', 'Ultra'])

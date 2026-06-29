from rest_framework import serializers
from hardware.models import HardwareComponent, PCBuild

class HardwareComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareComponent
        fields = '__all__'

class PCBuildSerializer(serializers.ModelSerializer):
    cpu_details = HardwareComponentSerializer(source='cpu', read_only=True)
    gpu_details = HardwareComponentSerializer(source='gpu', read_only=True)
    ram_details = HardwareComponentSerializer(source='ram', read_only=True)
    motherboard_details = HardwareComponentSerializer(source='motherboard', read_only=True)
    psu_details = HardwareComponentSerializer(source='psu', read_only=True)
    storage_details = HardwareComponentSerializer(source='storage', read_only=True)

    class Meta:
        model = PCBuild
        fields = [
            'id', 'cpu', 'gpu', 'ram', 'motherboard', 'psu', 'storage',
            'cpu_details', 'gpu_details', 'ram_details', 'motherboard_details', 
            'psu_details', 'storage_details', 'total_cost', 'created_at', 'user'
        ]
        read_only_fields = ['total_cost', 'created_at']

class OptimizeBuildRequestSerializer(serializers.Serializer):
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1000)
    resolution = serializers.ChoiceField(choices=['1080p', '1440p', '4K'], default='1080p')
    quality_preset = serializers.ChoiceField(choices=['Low', 'Medium', 'High', 'Ultra'], default='Medium')
    priority = serializers.ChoiceField(choices=['cost-benefit', 'performance', 'balance'], default='balance')

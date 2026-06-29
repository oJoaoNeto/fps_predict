from django.db import models
from games.models import Game
from hardware.models import HardwareComponent

class FpsPrediction(models.Model):
    RESOLUTION_CHOICES = [
        ('1080p', '1920x1080'),
        ('1440p', '2560x1440'),
        ('4K', '3840x2160'),
    ]
    QUALITY_CHOICES = [
        ('Low', 'Low Settings'),
        ('Medium', 'Medium Settings'),
        ('High', 'High Settings'),
        ('Ultra', 'Ultra Settings'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='predictions')
    cpu = models.ForeignKey(HardwareComponent, on_delete=models.CASCADE, related_name='predictions_as_cpu')
    gpu = models.ForeignKey(HardwareComponent, on_delete=models.CASCADE, related_name='predictions_as_gpu')
    ram_gb = models.IntegerField()
    resolution = models.CharField(max_length=10, choices=RESOLUTION_CHOICES)
    quality_preset = models.CharField(max_length=10, choices=QUALITY_CHOICES)
    predicted_fps = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game.name} on {self.cpu.name}/{self.gpu.name} - {self.resolution}/{self.quality_preset}: {self.predicted_fps:.1f} FPS"

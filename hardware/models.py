from django.db import models
from django.contrib.auth.models import User

class HardwareComponent(models.Model):
    CATEGORY_CHOICES = [
        ('CPU', 'Processor'),
        ('GPU', 'Graphics Card'),
        ('RAM', 'Memory'),
        ('MOBO', 'Motherboard'),
        ('PSU', 'Power Supply'),
        ('STORAGE', 'Storage'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop_link = models.URLField(max_length=500, null=True, blank=True)
    specs = models.JSONField(default=dict, blank=True, help_text="Detalhes específicos como socket, TDP, vram, frequency, score (pontuação de benchmark).")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category}: {self.name}"

class PCBuild(models.Model):
    cpu = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_cpu')
    gpu = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_gpu')
    ram = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_ram')
    motherboard = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_mobo')
    psu = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_psu')
    storage = models.ForeignKey(HardwareComponent, on_delete=models.PROTECT, related_name='builds_as_storage')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='builds')

    def __str__(self):
        return f"Build #{self.id} - Total: R$ {self.total_cost}"

from django.test import TestCase
from decimal import Decimal
from hardware.models import HardwareComponent
from hardware.optimizer import find_best_build, OptimizationError

class HardwareOptimizerTestCase(TestCase):
    def setUp(self):
        self.cpu_am4 = HardwareComponent.objects.create(
            name="Ryzen 5 5600", category="CPU", price=Decimal("800.00"),
            specs={"socket": "AM4", "tdp": 65, "score": 21000}
        )
        self.cpu_intel = HardwareComponent.objects.create(
            name="Intel Core i5-12400F", category="CPU", price=Decimal("850.00"),
            specs={"socket": "LGA1700", "tdp": 65, "score": 20000}
        )
        
        self.gpu_mid = HardwareComponent.objects.create(
            name="RX 6600", category="GPU", price=Decimal("1300.00"),
            specs={"tdp": 132, "vram": 8, "score": 14000}
        )
        self.gpu_high = HardwareComponent.objects.create(
            name="RTX 4070", category="GPU", price=Decimal("3800.00"),
            specs={"tdp": 200, "vram": 12, "score": 27000}
        )
        
        self.mobo_am4 = HardwareComponent.objects.create(
            name="B450M", category="MOBO", price=Decimal("450.00"),
            specs={"socket": "AM4"}
        )
        self.mobo_intel = HardwareComponent.objects.create(
            name="H610M", category="MOBO", price=Decimal("500.00"),
            specs={"socket": "LGA1700"}
        )
        
        self.ram_8 = HardwareComponent.objects.create(
            name="8GB RAM", category="RAM", price=Decimal("160.00"),
            specs={"size_gb": 8}
        )
        self.ram_16 = HardwareComponent.objects.create(
            name="16GB RAM", category="RAM", price=Decimal("320.00"),
            specs={"size_gb": 16}
        )
        
        self.psu_450 = HardwareComponent.objects.create(
            name="450W PSU", category="PSU", price=Decimal("280.00"),
            specs={"wattage": 450}
        )
        self.psu_650 = HardwareComponent.objects.create(
            name="650W PSU", category="PSU", price=Decimal("350.00"),
            specs={"wattage": 650}
        )
        
        self.storage_ssd = HardwareComponent.objects.create(
            name="SSD 240GB", category="STORAGE", price=Decimal("150.00"),
            specs={"size_gb": 240}
        )

    def test_optimizer_respects_budget(self):
        budget = Decimal("3500.00")
        build = find_best_build(budget, priority="balance")
        
        self.assertIsNotNone(build)
        self.assertLessEqual(build['total_cost'], budget)
        self.assertEqual(build['cpu'].specs['socket'], build['motherboard'].specs['socket'])
        self.assertGreaterEqual(float(build['psu'].specs['wattage']), 65 + 132 + 150)

    def test_optimizer_socket_compatibility(self):
        HardwareComponent.objects.filter(category="MOBO", name="H610M").delete()
        HardwareComponent.objects.filter(category="CPU", name="Ryzen 5 5600").delete()
        
        with self.assertRaises(OptimizationError):
            find_best_build(Decimal("5000.00"))

    def test_optimizer_insufficient_budget(self):
        with self.assertRaises(OptimizationError):
            find_best_build(Decimal("1000.00"))

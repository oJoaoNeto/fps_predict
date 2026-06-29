from django.core.management.base import BaseCommand
from games.models import Game
from hardware.models import HardwareComponent

class Command(BaseCommand):
    help = 'Preenche o banco de dados com peças de hardware realistas com especificações para o ML e o jogo CS:GO'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando o seed do banco de dados com especificações completas para Machine Learning...')
        
        # 1. Seed de Jogos
        game, created = Game.objects.get_or_create(
            steam_id='730',
            defaults={
                'name': 'Counter-Strike: Global Offensive / CS2',
                'genre': 'Action, FPS',
                'cover_image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg',
                'min_requirements': {
                    'os': 'Windows® 10',
                    'processor': 'Intel® Core™ i5 750 or AMD Phenom™ II X4 955',
                    'memory': '8 GB RAM',
                    'graphics': 'DirectX 11, Shader Model 5.0 compatible video card with 1 GB or more VRAM',
                    'storage': '85 GB available space'
                },
                'rec_requirements': {
                    'os': 'Windows® 10/11 64-bit',
                    'processor': 'Intel® Core™ i7 9700k or AMD Ryzen™ 7 3700X',
                    'memory': '16 GB RAM',
                    'graphics': 'DirectX 12 compatible video card with 6 GB VRAM',
                    'storage': '85 GB available SSD space'
                }
            }
        )
        if created:
            self.stdout.write(f"Jogo '{game.name}' adicionado com sucesso.")
        else:
            self.stdout.write(f"Jogo '{game.name}' já existia no banco.")

        # 2. Seed de Componentes de Hardware
        hardware_list = [
            # === CPUs ===
            {
                'name': 'Ryzen 3 4100 (3.8GHz)',
                'category': 'CPU',
                'price': 400.00,
                'specs': {
                    'socket': 'AM4', 'tdp': 65, 'score': 11000,
                    'CpuFrequency': 3600, 'CpuTurboClock': 4000,
                    'CpuNumberOfCores': 4, 'CpuNumberOfThreads': 8,
                    'CpuBaseClock': 100, 'CpuCacheL2': 2, 'CpuCacheL3': 4,
                    'CpuProcessSize': 7, 'CpuNumberOfTransistors': 4800
                }
            },
            {
                'name': 'Ryzen 5 5600 (3.5GHz)',
                'category': 'CPU',
                'price': 800.00,
                'specs': {
                    'socket': 'AM4', 'tdp': 65, 'score': 21000,
                    'CpuFrequency': 3500, 'CpuTurboClock': 4400,
                    'CpuNumberOfCores': 6, 'CpuNumberOfThreads': 12,
                    'CpuBaseClock': 100, 'CpuCacheL2': 3, 'CpuCacheL3': 32,
                    'CpuProcessSize': 7, 'CpuNumberOfTransistors': 10700
                }
            },
            {
                'name': 'Ryzen 7 5700X (3.4GHz)',
                'category': 'CPU',
                'price': 1200.00,
                'specs': {
                    'socket': 'AM4', 'tdp': 65, 'score': 26000,
                    'CpuFrequency': 3400, 'CpuTurboClock': 4600,
                    'CpuNumberOfCores': 8, 'CpuNumberOfThreads': 16,
                    'CpuBaseClock': 100, 'CpuCacheL2': 4, 'CpuCacheL3': 32,
                    'CpuProcessSize': 7, 'CpuNumberOfTransistors': 10700
                }
            },
            {
                'name': 'Intel Core i5-12400F (2.5GHz)',
                'category': 'CPU',
                'price': 850.00,
                'specs': {
                    'socket': 'LGA1700', 'tdp': 65, 'score': 20000,
                    'CpuFrequency': 2500, 'CpuTurboClock': 4400,
                    'CpuNumberOfCores': 6, 'CpuNumberOfThreads': 12,
                    'CpuBaseClock': 100, 'CpuCacheL2': 7.5, 'CpuCacheL3': 18,
                    'CpuProcessSize': 10, 'CpuNumberOfTransistors': 12000
                }
            },
            {
                'name': 'Intel Core i7-13700K (3.4GHz)',
                'category': 'CPU',
                'price': 2400.00,
                'specs': {
                    'socket': 'LGA1700', 'tdp': 125, 'score': 34000,
                    'CpuFrequency': 3400, 'CpuTurboClock': 5400,
                    'CpuNumberOfCores': 16, 'CpuNumberOfThreads': 24,
                    'CpuBaseClock': 100, 'CpuCacheL2': 24, 'CpuCacheL3': 30,
                    'CpuProcessSize': 10, 'CpuNumberOfTransistors': 25000
                }
            },

            # === GPUs ===
            {
                'name': 'GTX 1650 (4GB)',
                'category': 'GPU',
                'price': 900.00,
                'specs': {
                    'tdp': 75, 'score': 7800,
                    'GpuBoostClock': 1665, 'GpuBaseClock': 1485,
                    'GpuMemoryBus': 128, 'GpuMemorySize': 4,
                    'GpuBandwidth': 128000, 'GpuNumberOfShadingUnits': 896,
                    'GpuNumberOfROPs': 32, 'GpuNumberOfTMUs': 56,
                    'GpuFP32Performance': 2984, 'GpuNumberOfTransistors': 4700,
                    'GpuPixelRate': 53280, 'GpuTextureRate': 93240,
                    'GpuDieSize': 200, 'GpuProcessSize': 12,
                    'GpuArchScore': 12, 'GpuMemTypeScore': 2
                }
            },
            {
                'name': 'RX 580 (8GB)',
                'category': 'GPU',
                'price': 600.00,
                'specs': {
                    'tdp': 185, 'score': 8500,
                    'GpuBoostClock': 1340, 'GpuBaseClock': 1257,
                    'GpuMemoryBus': 256, 'GpuMemorySize': 8,
                    'GpuBandwidth': 256000, 'GpuNumberOfShadingUnits': 2304,
                    'GpuNumberOfROPs': 32, 'GpuNumberOfTMUs': 144,
                    'GpuFP32Performance': 6175, 'GpuNumberOfTransistors': 5700,
                    'GpuPixelRate': 42880, 'GpuTextureRate': 192960,
                    'GpuDieSize': 232, 'GpuProcessSize': 14,
                    'GpuArchScore': 8, 'GpuMemTypeScore': 2
                }
            },
            {
                'name': 'RX 6600 (8GB)',
                'category': 'GPU',
                'price': 1300.00,
                'specs': {
                    'tdp': 132, 'score': 14000,
                    'GpuBoostClock': 2491, 'GpuBaseClock': 1626,
                    'GpuMemoryBus': 128, 'GpuMemorySize': 8,
                    'GpuBandwidth': 224000, 'GpuNumberOfShadingUnits': 1792,
                    'GpuNumberOfROPs': 64, 'GpuNumberOfTMUs': 112,
                    'GpuFP32Performance': 8928, 'GpuNumberOfTransistors': 11060,
                    'GpuPixelRate': 159400, 'GpuTextureRate': 279000,
                    'GpuDieSize': 237, 'GpuProcessSize': 7,
                    'GpuArchScore': 13, 'GpuMemTypeScore': 4
                }
            },
            {
                'name': 'RTX 3060 (12GB)',
                'category': 'GPU',
                'price': 1800.00,
                'specs': {
                    'tdp': 170, 'score': 13500,
                    'GpuBoostClock': 1777, 'GpuBaseClock': 1320,
                    'GpuMemoryBus': 192, 'GpuMemorySize': 12,
                    'GpuBandwidth': 360000, 'GpuNumberOfShadingUnits': 3584,
                    'GpuNumberOfROPs': 48, 'GpuNumberOfTMUs': 112,
                    'GpuFP32Performance': 12740, 'GpuNumberOfTransistors': 12000,
                    'GpuPixelRate': 85300, 'GpuTextureRate': 199000,
                    'GpuDieSize': 276, 'GpuProcessSize': 8,
                    'GpuArchScore': 14, 'GpuMemTypeScore': 4
                }
            },
            {
                'name': 'RTX 4070 (12GB)',
                'category': 'GPU',
                'price': 3800.00,
                'specs': {
                    'tdp': 200, 'score': 27000,
                    'GpuBoostClock': 2475, 'GpuBaseClock': 1920,
                    'GpuMemoryBus': 192, 'GpuMemorySize': 12,
                    'GpuBandwidth': 504000, 'GpuNumberOfShadingUnits': 5888,
                    'GpuNumberOfROPs': 64, 'GpuNumberOfTMUs': 184,
                    'GpuFP32Performance': 29150, 'GpuNumberOfTransistors': 35800,
                    'GpuPixelRate': 158400, 'GpuTextureRate': 455400,
                    'GpuDieSize': 295, 'GpuProcessSize': 5,
                    'GpuArchScore': 14, 'GpuMemTypeScore': 4
                }
            },

            # === Motherboards (MOBO) ===
            {
                'name': 'Gigabyte B450M DS3H V2',
                'category': 'MOBO',
                'price': 450.00,
                'specs': {'socket': 'AM4'}
            },
            {
                'name': 'MSI MAG B550M Bazooka',
                'category': 'MOBO',
                'price': 750.00,
                'specs': {'socket': 'AM4'}
            },
            {
                'name': 'Asus Prime H610M-K DDR4',
                'category': 'MOBO',
                'price': 500.00,
                'specs': {'socket': 'LGA1700'}
            },
            {
                'name': 'Gigabyte B760M Aorus Elite',
                'category': 'MOBO',
                'price': 1100.00,
                'specs': {'socket': 'LGA1700'}
            },

            # === RAM ===
            {
                'name': 'Kingston Fury Beast 8GB DDR4 3200MHz',
                'category': 'RAM',
                'price': 160.00,
                'specs': {'size_gb': 8}
            },
            {
                'name': 'Corsair Vengeance LPX 16GB (2x8GB) DDR4 3200MHz',
                'category': 'RAM',
                'price': 320.00,
                'specs': {'size_gb': 16}
            },
            {
                'name': 'Corsair Vengeance LPX 32GB (2x16GB) DDR4 3200MHz',
                'category': 'RAM',
                'price': 650.00,
                'specs': {'size_gb': 32}
            },

            # === PSU ===
            {
                'name': 'Corsair CV450 450W 80 Plus Bronze',
                'category': 'PSU',
                'price': 280.00,
                'specs': {'wattage': 450}
            },
            {
                'name': 'MSI MAG A650BN 650W 80 Plus Bronze',
                'category': 'PSU',
                'price': 350.00,
                'specs': {'wattage': 650}
            },
            {
                'name': 'XPG Core Reactor 850W 80 Plus Gold',
                'category': 'PSU',
                'price': 700.00,
                'specs': {'wattage': 850}
            },

            # === STORAGE ===
            {
                'name': 'Crucial BX500 240GB SATA SSD',
                'category': 'STORAGE',
                'price': 150.00,
                'specs': {'size_gb': 240}
            },
            {
                'name': 'Kingston NV2 500GB M.2 NVMe SSD',
                'category': 'STORAGE',
                'price': 250.00,
                'specs': {'size_gb': 500}
            },
            {
                'name': 'Kingston NV2 1TB M.2 NVMe SSD',
                'category': 'STORAGE',
                'price': 400.00,
                'specs': {'size_gb': 1000}
            },
        ]

        count = 0
        for item in hardware_list:
            comp, created = HardwareComponent.objects.update_or_create(
                name=item['name'],
                category=item['category'],
                defaults={
                    'price': item['price'],
                    'specs': item['specs'],
                    'shop_link': f"https://www.google.com/search?q={item['name'].replace(' ', '+')}",
                    'is_active': True
                }
            )
            if created:
                count += 1
                
        self.stdout.write(self.style.SUCCESS(f"Seed concluído! {count} novos componentes adicionados e todos atualizados com especificações para ML."))

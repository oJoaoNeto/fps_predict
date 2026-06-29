from django.test import TestCase
from prediction.predictor import predict_fps

class FpsPredictorTestCase(TestCase):
    def setUp(self):
        self.cpu_low = {'score': 8000}
        self.cpu_high = {'score': 25000}
        self.gpu_low = {'score': 6000}
        self.gpu_high = {'score': 18000}

    def test_fps_varies_with_hardware(self):
        fps_low = predict_fps("CS:GO", self.cpu_low, self.gpu_low, 8, "1080p", "Medium")
        fps_high = predict_fps("CS:GO", self.cpu_high, self.gpu_high, 16, "1080p", "Medium")
        
        self.assertGreater(fps_high, fps_low)

    def test_fps_varies_with_resolution(self):
        fps_1080p = predict_fps("CS:GO", self.cpu_high, self.gpu_high, 16, "1080p", "Medium")
        fps_4k = predict_fps("CS:GO", self.cpu_high, self.gpu_high, 16, "4K", "Medium")
        
        self.assertLess(fps_4k, fps_1080p)

    def test_fps_varies_with_quality(self):
        fps_low_settings = predict_fps("CS:GO", self.cpu_high, self.gpu_high, 16, "1080p", "Low")
        fps_ultra_settings = predict_fps("CS:GO", self.cpu_high, self.gpu_high, 16, "1080p", "Ultra")
        
        self.assertLess(fps_ultra_settings, fps_low_settings)

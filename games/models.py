from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    steam_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    cover_image_url = models.URLField(max_length=500, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    min_requirements = models.JSONField(default=dict, blank=True)
    rec_requirements = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

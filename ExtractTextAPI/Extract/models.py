from django.db import models

# Create your models here.

class Extract(models.Model):
    detail = models.CharField(max_length=70, blank=False, default='')
    file = models.FileField(upload_to="my_file", blank=True)
    
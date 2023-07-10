from django.db import models

# Create your models here.

class OCR(models.Model):
    base64_data = models.TextField(blank=False, default='')
    
    # def __str__(self):
    #     return self.base64_data[:50]  
    # # Return a truncated version of the base64 data for display 
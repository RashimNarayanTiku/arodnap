from django.db import models
from django.conf import settings
from datetime import datetime

class Entry(models.Model):

    title = models.CharField(max_length=150,default='')
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner}: {self.title}'

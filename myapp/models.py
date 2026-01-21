from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(blank=False)
    status = models.CharField(choices={'pending': 'pending', 'started': 'started', 'done': 'done'}, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


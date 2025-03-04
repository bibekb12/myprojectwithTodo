from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.task
        
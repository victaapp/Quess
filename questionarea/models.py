from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(blank=True, null=True, auto_now_add=True)
    last_modified = models.DateField(blank=True, null=True, auto_now=True)
    ask_by = models.ForeignKey(User, related_name="aks_by", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ask_by.username} : {self.title[:50]}"



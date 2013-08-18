from django.db import models

# Create your models here.
class MOOC_User(models.Model):
    primaryURL = models.CharField(max_length=200)
    secondaryURL = models.CharField(max_length=200)
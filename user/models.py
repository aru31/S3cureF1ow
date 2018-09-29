from django.db import models
from django.contrib.auth.models import User


## Sample just for AAdhaar
class Identity(models.Model):
    identity = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=511)
    gender = models.CharField(max_length=511)
    address = models.CharField(max_length=1023)
    aadhar_number = models.CharField(max_length=12)
    files = models.FileField()

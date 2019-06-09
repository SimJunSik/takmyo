from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser) :
    
    gender = models.CharField(max_length=10, default='unknown')
    address = models.CharField(max_length=255, default='unknown')
    detail_address = models.CharField(max_length=255, default='unknown')
    extra_address = models.CharField(max_length=255, default='unknown')
    phone = models.CharField(max_length=20, default='unknown')
    check_phone = models.BooleanField(default=False)
    is_catsitter = models.BooleanField(default=False)
    is_catee = models.BooleanField(default=False)

    def __str__(self) :

        return self.username
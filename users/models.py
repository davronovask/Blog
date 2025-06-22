from django.contrib.auth.models import AbstractUser
from django.db import models
from users.manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

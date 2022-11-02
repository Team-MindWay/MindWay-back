from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    first_name = None
    last_name = None

    def __str__(self) -> str:
        return self.username

class Refresh(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.username} refresh"
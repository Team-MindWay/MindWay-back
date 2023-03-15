from django.db import models
from apps.user.accounts.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    url = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.title}'
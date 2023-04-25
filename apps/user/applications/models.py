from django.db import models
from apps.user.accounts.models import User

CATEGORY = (
    ('novel', 'novel'),
    ('essey', 'essay'),
)

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    url = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.title}'

class Recommend(models.Model):
    recommender = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    outline = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=CATEGORY, default=None, null=True)

    def __str__(self) -> str:
        return f'{self.recommender.username} - {self.title}'
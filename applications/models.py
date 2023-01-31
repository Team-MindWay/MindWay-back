from django.db import models
from accounts.models import User

LIBRARY_CATEGORY = (
    ('온라인 강의실', '온라인 강의싷'),
    ('학부모 회의실', '학부모 회의실'),
    ('스터디 카페', '스터디 카페')
)
# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    url = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.title}'

class Library(models.Model):
    team = models.CharField(max_length=50, unique=True)
    room = models.CharField(max_length=20, choices=LIBRARY_CATEGORY)
    
    def __str__(self) -> str:
        return f'({self.room}) {self.team}'

class TeamMember(models.Model):
    team = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='student')
    number = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.team.team} - {self.number} {self.name}'
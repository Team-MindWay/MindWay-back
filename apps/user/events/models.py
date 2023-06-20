from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField()

    def __str__(self) -> str:
        return f'{self.title}'
    
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self) -> str:
        return f'{self.event.title} image'
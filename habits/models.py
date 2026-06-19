from django.db import models
from django.conf import settings
from django.utils import timezone

class Habit(models.Model):
    "Habit with repetion frequency"

    class Frequensy(models.TextChoices):
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"
        CUSTOM = "CUSTOM"

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    frequensy = models.CharField(
        max_length=10,
        choices=Frequensy.choices,
        default=Frequensy.DAILY,
    )

    # participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
    

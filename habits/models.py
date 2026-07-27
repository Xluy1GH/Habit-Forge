from django.db import models
from django.conf import settings
from django.utils import timezone

from django_celery_beat.models import IntervalSchedule, PeriodicTask

class Habit(models.Model):
    "Habit with repetition frequency"

    title = models.CharField(max_length=50)

    description = models.TextField(max_length=200)

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    # Linking the frequency from the model to the django-celery-beat scheduler periods
    class Frequency(models.TextChoices):
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"

    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.DAILY,
    )

    CELERY_SCHEDULE_MAP = {
        "DAILY": {"every": 1, "period": IntervalSchedule.DAYS},
        "WEEKLY": {"every": 7, "period": IntervalSchedule.DAYS},
    }


    # participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    pub_date = models.DateTimeField(default=timezone.now())

    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # If the habit is new, create a corresponding periodic task in django-celery-beat
        if is_new:
            schedule, created = IntervalSchedule.objects.get_or_create(
                **self.CELERY_SCHEDULE_MAP[self.frequency]
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name="Send telegram message",
                task="habits.tasks.send_telegram_message",
            )

    def __str__(self):
        return self.title
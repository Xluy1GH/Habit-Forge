from django.db import models
from django.conf import settings
from django.utils import timezone

from django_celery_beat.models import IntervalSchedule, PeriodicTask

import json

class Habit(models.Model):
    # Habit with repetition frequency
    title = models.CharField(max_length=50)
    description = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(default=timezone.now)

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


    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # If the habit is new, create a corresponding periodic task in django-celery-beat
        if is_new:
            schedule, created = IntervalSchedule.objects.get_or_create(
                **self.CELERY_SCHEDULE_MAP[self.frequency]
            )

            task_kwargs = json.dumps({'habit_id': self.id})

            PeriodicTask.objects.create(
                interval=schedule,
                name=f"Habit {self.id} Notify {self.title}",
                task="habits.tasks.send_telegram_message",
                kwargs=task_kwargs,
            )

    def __str__(self):
        return self.title

class UserHabit(models.Model):
    # An intermediate model between user and habit
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_habits",
        )
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="followers",
        )

    # User's statistics
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.habit.title}"
    
from django.contrib import admin
from .models import Habit

class HabitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Habit, HabitAdmin)
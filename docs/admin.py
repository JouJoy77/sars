from django.contrib import admin
from .models import AvailableAchievement, LevelChoice, RoleChoice, ActivityChoice, Achievement

# Register your models here.
admin.site.register(AvailableAchievement)
admin.site.register(LevelChoice)
admin.site.register(ActivityChoice)
admin.site.register(RoleChoice)
admin.site.register(Achievement)
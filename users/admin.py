from django.contrib import admin
from .models import Profile, User

#доступ моделей для просмотра в системе администрирования Django
admin.site.register(Profile)
admin.site.register(User)
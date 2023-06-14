from django.contrib import admin
from .models import Profile, User, Role

#доступ моделей для просмотра в системе администрирования Django
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Role)
from django.contrib.auth.models import Permission
from .models import Role

# Создание группы роли "Модератор"
moderator_group, created = Role.objects.get_or_create(name='Модератор')
# Назначение разрешений
moderator_group.permissions.add(
    Permission.objects.get(codename='add_post')
)

# Создание группы роли "Руководитель"
manager_group, created = Role.objects.get_or_create(name='Руководитель')
# Назначение разрешений
manager_group.permissions.add(
    Permission.objects.get(codename='add_department')
)

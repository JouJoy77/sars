from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import Group
import re

class Role(Group):
    pass

#вспомогательный класс-менеджер для использования модели пользователей
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Отсутствует адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email,username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь поле is_staff==True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь поле is_superuser==True.')

        return self._create_user(email, password, **extra_fields)

#модель пользователя
class User(AbstractUser):
    role_status = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_role')
    email = models.EmailField(('email address'), max_length=40, unique=True)
    username = models.CharField(max_length=40)
    snils = models.CharField(max_length=14, unique=True)
    rating = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(blank=True, default=0, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'

#модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} Profile'

#функция автосоздания профиля при регистрации
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

@receiver(pre_save, sender=User)
def format_snils(sender, instance, **kwargs):
    # Преобразование СНИЛС в нужный формат XXX-XXX-XXX YY
    snils = instance.snils
    # Удаляем все нецифровые символы
    snils = re.sub(r'\D', '', snils)
    # Форматируем номер СНИЛС
    formatted_snils = f'{snils[:3]}-{snils[3:6]}-{snils[6:9]} {snils[9:11]}'
    # Обновляем значение поля snils
    instance.snils = formatted_snils

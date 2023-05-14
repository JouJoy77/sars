from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.urls import reverse

# from django.utils.translation import ugettext_lazy as _

class Achievement(models.Model):
    """Достижение, доступное для получения"""
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        null=True
    )
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=5, null=True)


    class Meta:
        verbose_name = 'Талоны пользователей'
        verbose_name_plural = 'Талоны пользователей'

    def __str__(self) -> str:
        return f'{self.user_id} - {self.title}/{str(self.id_for_use)[-4:]}'

#вспомогательный класс-менеджер для использования модели пользователей
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Отсутствует адрес электронной почты')
        email = self.normalize_email(email)
        user = self.model(email=email,username=models.CharField(default=email), **extra_fields)
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

    email = models.EmailField(('email address'), max_length=40, unique=True)
    username = models.CharField(max_length=40)
    snils = models.CharField(max_length=20, unique=True)
    rating = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(blank=True, default=0)

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

class AchievementOfUser(models.Model):
    """Достижение пользователя"""
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Покупатель')
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        null=True
    )
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=5, null=True)

    class Meta:
        verbose_name = 'Талоны пользователей'
        verbose_name_plural = 'Талоны пользователей'

    def __str__(self) -> str:
        return f'{self.user_id} - {self.title}/{str(self.id_for_use)[-4:]}'
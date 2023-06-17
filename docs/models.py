from django.db import models
from users.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# модель для выбора типа деятельности
class ActivityChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# модель для выбора уровня мероприятия
class LevelChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name    

# модель для выбора роли студента в мероприятии
class RoleChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class AvailableAchievement(models.Model):
    """Модель для добавления всевозможных комбинаций по уровню, роли и типу деятельности."""
    title = models.CharField(verbose_name='Краткое название', max_length=70)
    activity = models.ForeignKey(to=ActivityChoice, on_delete=models.CASCADE, verbose_name='Тип деятельности')
    level = models.ForeignKey(to=LevelChoice, on_delete=models.CASCADE, verbose_name='Уровень мероприятия')
    role = models.ForeignKey(to=RoleChoice, on_delete=models.CASCADE, verbose_name='Роль студента (участник или организатор)')
    points = models.IntegerField(verbose_name='Баллы')
    
    class Meta:
        verbose_name = 'Доступное к выбору достижение'
        verbose_name_plural = 'Все доступные к выбору достижения'
    
    def __str__(self):
        return self.title

class Achievement(models.Model):
    """Модель для хранения документов и достижений."""
    title = models.CharField(verbose_name='Краткое название', max_length=70)
    picture = models.ImageField(upload_to='images/', verbose_name='Грамота, диплом, справка', null = True,
                                validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'jpeg'))])
    user = models.ForeignKey(to=User, related_name='user', on_delete=models.CASCADE,  blank=True)
    achievement = models.ForeignKey(to=AvailableAchievement, on_delete=models.CASCADE, verbose_name='Достижение или деятельность')
    is_moderated = models.BooleanField(verbose_name='Проверено модератором', default=False)
    is_accepted = models.BooleanField(verbose_name='Подтверждено системой', default=False)
    is_rejected = models.BooleanField(verbose_name='Отклонено модератором', default=False)
    
    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'

    # функция для получения баллов за достижение
    @property
    def get_points(self):
        return self.achievement.points if ((self.is_moderated or self.is_accepted) and not self.is_rejected) else 0
 
    @property
    def get_picture(self):
        """
        Получение заглушки при отсутсвии изображения
        """
        return '/images/notfound.png' if not self.picture else self.picture

    def __str__(self):
        return self.title


@receiver(post_save, sender=Achievement)
def update_user_rating(sender, instance, created, **kwargs):
    # Если достижение не было проверено, то запускается автоматическая проверка
    if not (instance.is_moderated or instance.is_accepted or instance.is_rejected):
        #Для избежания кругового импорта используется частичный импорт
        from .pic_reader import check_doc
        check_doc(instance.id)
    else:
        # При сохранении достижения предполагается изменение баллов пользователя
        user = instance.user
        total_points = Achievement.objects.filter(
            user=user, is_accepted=True).aggregate(
                total_points=models.Sum('achievement__points'))['total_points']
        user.points = total_points or 0
        user.save()
        #Получаем всех пользователей и обновляем их рейтинг
        users = User.objects.order_by('-points')
        for rank, user in enumerate(users, start=1):
            user.rating = rank
            user.save()
    
# Регистрация сигнала
post_save.connect(update_user_rating, sender=Achievement)

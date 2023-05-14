from django.db import models
from users.models import User


class ActivityChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class LevelChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class RoleChoice(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class AvailableAchievement(models.Model):
    """Модель для добавления всевозможных комбинаций по уровню, роли и типу деятельности."""
    title = models.TextField(verbose_name='Краткое название')
    activity = models.ForeignKey(to=ActivityChoice, on_delete=models.CASCADE, verbose_name='Тип деятельности')
    level = models.ForeignKey(to=LevelChoice, on_delete=models.CASCADE, verbose_name='Уровень мероприятия')
    role = models.ForeignKey(to=RoleChoice, on_delete=models.CASCADE, verbose_name='Роль студента (участник или организатор)')
    points = models.IntegerField(verbose_name='Баллы')


class Achievement(models.Model):
    """Модель для хранения документов и достижений."""
    title = models.TextField(verbose_name='Краткое название')
    picture = models.ImageField(upload_to='images/', verbose_name='Грамота, диплом, справка')
    user = models.ForeignKey(to=User, related_name='document', on_delete=models.CASCADE)
    achievement = models.ForeignKey(to=AvailableAchievement, on_delete=models.CASCADE, verbose_name='Достижение или деятельность')
    points = models.IntegerField(verbose_name='Баллы')
    
    def calculate_points(self, level, role, activity):
        pass
        
    def save(self, *args, **kwargs):
        # Вычисление количества баллов и сохранение в поле "points"
        self.points = self.calculate_points(self.achievement.level, self.achievement.role, self.achievement.activity)
        super(Achievement, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

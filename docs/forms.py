from django import forms
from .models import Achievement
from .pic_reader import check_doc

from django import forms

class AchievementForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    class Meta:
        model = Achievement
        exclude = ['user', 'is_moderated', 'is_accepted', 'is_rejected']  # Исключение поля "user" из списка отображаемых полей
        
    def process_document(self):
        if self.is_valid():
            achievement = self.save(commit=False)
            achievement.save()  # Сохраняем объект Achievement
            check_doc.delay(achievement.id)  # Вызываем задачу Celery для обработки достижения
            return achievement
        else:
            return None
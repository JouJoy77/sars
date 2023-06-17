from django import forms
from .models import Achievement
from django import forms

class AchievementForm(forms.ModelForm):
    picture = forms.ImageField(required=False, label='Грамота, диплом, справка')
    class Meta:
        model = Achievement
        exclude = ['user', 'is_moderated', 'is_accepted', 'is_rejected']  # Исключение поля "user" из списка отображаемых полей

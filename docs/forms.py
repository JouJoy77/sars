from django import forms
from .models import Achievement

from django import forms

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        exclude = ['user', 'is_moderated', 'is_accepted']  # Исключение поля "user" из списка отображаемых полей
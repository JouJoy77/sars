from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re

class SnilsField(forms.CharField):
    # специальное поле для СНИЛС
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = True
        self.regex = re.compile(r'^(\d{3}-\d{3}-\d{3} \d{2}|\d{11}|\d{3} \d{3} \d{3} \d{2})$')

    def clean(self, value):
        value = super().clean(value)
        # Удаляем все нецифровые символы
        value = re.sub(r'\D', '', value)
        # Проверяем длину введенного значения
        if len(value) != 11:
            raise forms.ValidationError('СНИЛС должен содержать 11 цифр')
        # Проверяем формат СНИЛС
        if not self.regex.match(value):
            raise forms.ValidationError('Некорректный формат СНИЛС')
        # Проверяем на повторяющиеся цифры
        for i in range(len(value) - 2):
            if value[i] == value[i + 1] == value[i + 2]:
                raise forms.ValidationError('Некорректный номер СНИЛС (повторяющаяся цифра)')
        # Проверяем контрольное число
        sum_ = sum(int(value[i]) * (9 - i) for i in range(9))
        check_digit = int(value[-2:])
        control_digit = (sum_ % 101) % 100
        if control_digit != check_digit:
            raise forms.ValidationError('Некорректное контрольное число СНИЛС')

        return value

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Ваша электронная почта'
        self.fields['password'].label = 'Ваш пароль'  # Измененная метка поля password

class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователей, используется для получения данных от пользователя."""
    email = forms.EmailField(label='Адрес электронной почты')
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=True, label='Фамилия')
    snils = SnilsField(label='СНИЛС (В формате XXX-XXX-XXX YY)')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        # Здесь можно указать только те поля, которые нам необходимы.
        fields = ['email', 'first_name', 'last_name', 'snils', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
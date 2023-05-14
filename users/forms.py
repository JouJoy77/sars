from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator




class SnilsWidget(forms.MultiWidget):
    """Виджет для получения СНИЛС."""
    def __init__(self, first_length=3, second_length=2, attrs=None):
        widgets = [forms.TextInput(attrs={'size': first_length, 'maxlength': first_length}),
                   forms.TextInput(attrs={'size': first_length, 'maxlength': first_length}),
                   forms.TextInput(attrs={'size': first_length, 'maxlength': first_length}),
                   forms.TextInput(attrs={'size': second_length, 'maxlength': second_length})]
        super(SnilsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.first, value.second, value.third, value.fourth]
        else:
            return ['0', '1', '2', '3', '4']
        
    def format_output(self, rendered_widgets):
        return f'{rendered_widgets[0]} - {rendered_widgets[1]} - {rendered_widgets[2]} {rendered_widgets[3]}'
    
    def render(self, name, value, attrs=None, renderer = None):
        """Просто html код, чтобы напрямую задать вид поля ввода СНИЛС."""
        htmltext = '<div id="div_id_snils" class="form-group"> <label class=" requiredField"></label>\
    <p>\
    \
   В формате (XXX-XXX-XXX XX)\
</p><div class="row gtr-uniform"><input class="col-1 col-12-small" type="text" name="snils_0"  size="3" maxlength="3" required="" id="id_snils_0">-<input class="col-1 col-12-xsmall" type="text" name="snils_1" size="3" maxlength="3" required="" id="id_snils_1">-<input class="col-1 col-12-xsmall" type="text" name="snils_2" size="3" maxlength="3" required="" id="id_snils_2">   <input class="col-1 col-12-xsmall" type="text" name="snils_3" size="2" maxlength="2" required="" id="id_snils_3"></div> </div>'
        return htmltext
    
class SnilsField(forms.MultiValueField):
    """Поле СНИЛС, в него передаются данные и проверяются на валидность."""
    def __init__(self, first_length, second_length, *args, **kwargs):
        list_fields = [
            forms.CharField(
                validators=[RegexValidator(fr'^[0-9]',
                    'Вводите только цифры от 0 до 9, по 3 цифры в первых трех полях, 2 цифры в последнем')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]',
                    'Вводите только цифры от 0 до 9, по 3 цифры в первых трех полях, 2 цифры в последнем')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]',
                    'Вводите только цифры от 0 до 9, по 3 цифры в первых трех полях, 2 цифры в последнем')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]',
                    'Вводите только цифры от 0 до 9, по 3 цифры в первых трех полях, 2 цифры в последнем')],
            ),]
        super(SnilsField, self).__init__(list_fields, widget=SnilsWidget(first_length, second_length), *args, **kwargs)

    def compress(self, values):
        """Метод сборки и задания нормального вида СНИЛС."""
        return f'{values[0]} - {values[1]} - {values[2]} {values[3]}'


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователей, используется для получения данных от пользователя."""
    email = forms.EmailField(label='Адрес электронной почты')
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=True, label='Фамилия')
    snils = SnilsField(required=True, label='СНИЛС', first_length=3, second_length=2)
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
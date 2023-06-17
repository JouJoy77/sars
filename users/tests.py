from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegistrationTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'testname',
            'last_name': 'testname',
            'snils': '142-854-255 64',
            'password1': 'testpassword8543495PASS',
            'password2': 'testpassword8543495PASS',
        }

    def test_registration_form(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_registration_failure(self):
        # Попытка зарегистрировать пользователя без указания электронной почты
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = ''
        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'This field is required.') 
        # Попытка зарегистрировать пользователя с неправильным подтверждением пароля
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'Пароли не совпадают.')
        # Попытка зарегистрировать пользователя с неправильным СНИЛС
        invalid_user_data = self.user_data.copy()
        invalid_user_data['snils'] = '111-111-111 44'
        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'snils', 'Некорректный номер СНИЛС (повторяющаяся цифра)')
        invalid_user_data = self.user_data.copy()
        invalid_user_data['snils'] = '142-854-255 63'
        response = self.client.post(self.register_url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'snils', 'Некорректное контрольное число СНИЛС')

    def test_user_created(self):
        response = self.client.post(self.register_url, self.user_data, follow=True)
        self.assertTrue(get_user_model().objects.filter(email=self.user_data['email']).exists()) # Проверка, что пользователь был успешно создан

        
    

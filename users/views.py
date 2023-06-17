# user/views.py
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from docs.models import Achievement
from users.models import Profile
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

# вьюшка для формы регистрации
def register(request):
    # разрешены только post методы
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                email = form.cleaned_data.get('email')
                messages.success(request, f'Создан аккаунт {email}!')
                return redirect('login')
            except IntegrityError:
                form.add_error('snils', 'Такой СНИЛС уже зарегистрирован.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# вьюшка для просмотря профиля, с декоратором только для залогиненных пользователей
@login_required
def profile(request):
    prof = Profile.objects.order_by('id')
    user_id = request.user.pk
    achievements = Achievement.objects.filter(user_id=user_id).all()
    context = {
        'Name': 'Профиль',
        'profiles': prof,
        'achievements': achievements
    }
    return render(request, 'profile.html', context)
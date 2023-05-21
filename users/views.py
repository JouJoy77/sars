# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from docs.models import Achievement
from .models import User

from users.models import Profile
from .forms import UserRegisterForm
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

#вьюшка для формы регистрации
def register(request):
    #разрешены только post методы
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Создан аккаунт {email}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

#вьюшка для просмотря профиля, с декоратором только для залогиненных пользователей
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

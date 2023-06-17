from django.http import JsonResponse
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import AchievementForm
from .models import Achievement, ActivityChoice

# класс вью для загрузки документов
class DownloadAchievementView(LoginRequiredMixin, CreateView):
    form_class = AchievementForm
    template_name = 'download.html'
    success_url = reverse_lazy('download_achieve')
    # переопределение функции валидации
    def form_valid(self, form):
        form.instance.user = self.request.user  # Установка значения поля "user"
        if not (achievement := form.instance):
            return self.form_invalid(form)
        achievement.save()
        return super().form_valid(form)

# класс вью для страницы модерации
class ModerateView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'moderate.html'
    context_object_name = 'achievements'

    def get_queryset(self):
        user = self.request.user
        if  user and user.role_status and user.role_status.name in ['Модератор', 'Руководитель']:
            # Фильтрация документов, не прошедших ручную проверку, для модераторов и руководителей
            queryset = Achievement.objects.filter(is_moderated=False, is_rejected=False)
        else:
            # Те же документы, но для обычного пользователя (только его)
            queryset = Achievement.objects.filter(user=user, is_moderated=False, is_accepted=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = ActivityChoice.objects.all()
        
        return context

def update_status(request):
    if request.method == 'POST':
        achievement_id = request.POST.get('achievement_id')
        is_accepted = request.POST.get('is_accepted')
        achievement = Achievement.objects.get(pk=achievement_id)
        is_accepted = is_accepted != 'false'
        achievement.is_moderated = is_accepted
        achievement.is_accepted = is_accepted
        achievement.is_rejected = not is_accepted
        achievement.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return redirect('moderate')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    else:
        return redirect('moderate')

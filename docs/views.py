from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import AchievementForm
from .models import Achievement, ActivityChoice

# class DownloadAchievementView(LoginRequiredMixin, CreateView):
#     form_class = AchievementForm
#     template_name = 'download.html'
#     success_url = reverse_lazy('download')
#     print("TRY DOWNLOAD 22")
    
#     # def form_valid(self, form):
#     #     form.instance.user = self.request.user
#     #     return super(DownloadAchievementView, self).form_valid(form)

#     def post(self, request, *args, **kwargs):
#         print("TRY DOWNLOAD")
#         if request.method == "POST":
#             achieveForm = AchievementForm(request.POST)
#             print(achieveForm.fields)
#             if achieveForm.is_valid():
#                 print("IS VALID")
#                 achieveForm.user = request.user
#                 achieveForm.save()
#                 print(achieveForm.fields)
#                 messages.success(request, 'Ссылка добавлена')
#         context = {}
#         if not request.user.is_authenticated:
#             raise Http404
#         # user_id = request.user.pk
#         # context['user'] = user_id

#         return render(request=request, template_name=self.template_name, context=context)
# @login_required
# def download_achieve(request):
#     if request.method == "POST":
#         achieveForm = AchievementForm(request.POST)
#         if achieveForm.is_valid():
#             instance = achieveForm.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             messages.success(request, f'Ссылка добавлена')
#     else:
#         achieveForm = AchievementForm()
#     return render(request=request, template_name='download.html', context={'form': achieveForm})
class DownloadAchievementView(LoginRequiredMixin, CreateView):
    form_class = AchievementForm
    template_name = 'download.html'
    success_url = reverse_lazy('download_achieve')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Установка значения поля "user"
        achievement = form.process_document()  # Вызов метода process_document
        if achievement:
            # Дополнительная логика, если необходимо
            return super().form_valid(form)
        else:
            # Логика при невалидной форме
            return self.form_invalid(form)
        return super().form_valid(form)
    
class ModerateView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'moderate.html'
    context_object_name = 'achievements'

    def get_queryset(self):
        user = self.request.user
        category = self.request.GET.get('activity')
        if  user and user.role_status and user.role_status.name in ['Модератор', 'Руководитель']:
            # Filter unmoderated and unaccepted documents
            queryset = Achievement.objects.filter(is_moderated=False, is_rejected=False)
            # if category:
            #     # Apply category filter using OR condition
            #     queryset = queryset.filter(Q(achievement__activity__name__icontains=category) | Q(achievement__title__icontains=category))
        else:
            # Filter user's documents that require moderation
            queryset = Achievement.objects.filter(user=user, is_moderated=False, is_accepted=False)

        return queryset
    
    # def post(self, request, *args, **kwargs):
    #     achievement_id = self.kwargs['achievement_id']
    #     achievement = Achievement.objects.get(pk=achievement_id)

    #     if 'approve' in request.POST:
    #         achievement.is_moderated = True
    #         achievement.is_accepted = True
    #         achievement.is_rejected = False
    #     elif 'reject' in request.POST:
    #         achievement.is_moderated = False
    #         achievement.is_accepted = False
    #         achievement.is_rejected = True

    #     achievement.save()

    #     return HttpResponseRedirect(reverse('moderate'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add AchievementAvailable queryset to the context
        context['activity'] = ActivityChoice.objects.all()
        
        return context
    
from django.http import JsonResponse


def update_status(request):
    if request.method == 'POST':
        achievement_id = request.POST.get('achievement_id')
        is_accepted = request.POST.get('is_accepted')
        achievement = Achievement.objects.get(pk=achievement_id)

        # if 'approve' in request.POST:
        achievement.is_moderated = bool(is_accepted)
        achievement.is_accepted = bool(is_accepted)
        achievement.is_rejected = not bool(is_accepted)
        # elif 'reject' in request.POST:

        achievement.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            # Возвращайте ответ в соответствии с вашими потребностями
            return redirect('moderate')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    else:
        # Возвращайте ответ в соответствии с вашими потребностями
        return redirect('moderate')

# def update_status(request):
#     print(request)
#     if request.method == 'POST' and request.is_ajax():
#         achievement_id = request.POST.get('achievement_id')
#         is_accepted = request.POST.get('is_accepted')
#         achievement = Achievement.objects.get(pk=achievement_id)

#         # if 'approve' in request.POST:
#         achievement.is_moderated = is_accepted
#         achievement.is_accepted = is_accepted
#         achievement.is_rejected = not is_accepted
#         # elif 'reject' in request.POST:

#         achievement.save()

#         return JsonResponse({'success': True})

#     return JsonResponse({'success': False})
from django.http import Http404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
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
        return super().form_valid(form)
    
class ModerateView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'moderate.html'
    context_object_name = 'achievements'

    def get_queryset(self):
        user = self.request.user
        category = self.request.GET.get('activity')
        if user.role_status in ['Модератор', 'Руководитель']:
            # Filter unmoderated and unaccepted documents
            queryset = Achievement.objects.filter(is_moderated=False, is_accepted=False)
            # if category:
            #     # Apply category filter using OR condition
            #     queryset = queryset.filter(Q(achievement__activity__name__icontains=category) | Q(achievement__title__icontains=category))
        else:
            # Filter user's documents that require moderation
            queryset = Achievement.objects.filter(user=user, is_moderated=False, is_accepted=False)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add AchievementAvailable queryset to the context
        context['activity'] = ActivityChoice.objects.all()
        
        return context
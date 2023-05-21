from django.http import Http404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import AchievementForm
from .models import Achievement

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
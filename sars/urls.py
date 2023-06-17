"""
URL configuration for sars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, re_path
from pathlib import Path
from main import views
from users import views as user_views
from django.contrib.auth import views as auth_views
from docs import views as docs_views
from django.conf import settings
from django.conf.urls.static import static


#пути сайта - ссылки и их отображения в формате
#ссылка - отображение - (имя)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('download/', docs_views.DownloadAchievementView.as_view(), name='download_achieve'),
    path('moderate/<int:achievement_id>/', docs_views.ModerateView.as_view(), name='moderate_accept'),
    path('moderate/', docs_views.ModerateView.as_view(), name='moderate'),
    path('update-status/', docs_views.update_status, name='update_status'),
    path('download_excel/', views.download_excel, name='download_excel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

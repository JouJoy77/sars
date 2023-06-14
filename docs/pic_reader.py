import easyocr
import re
from django.db import models
from users.models import User
from pathlib import Path
import os
from celery import shared_task
from .models import Achievement


BASE_DIR = Path(__file__).resolve().parent.parent


def make_one_str(list_of_text):
    # Сделать список слов одной большой строкой
    return ''.join(list_of_text)
    

def preprocess_text(text):
    # Удалить все символы, кроме букв и цифр
    text = re.sub(r'[^\w\s]', '', text)
    
    # Привести текст к нижнему регистру
    text = text.lower()
    
    return text


def text_recognition(filename):
    # Распознать текст с картинки
    reader = easyocr.Reader(["ru", "en"])

    return reader.readtext(
        os.path.join(BASE_DIR/'media/', filename), detail=0, paragraph=True
    )


def get_text_from_picture(file):
    print("Я ПЫТАЮСЬ ОБРАБОТАТЬ ФАЙЛ")
    return make_one_str(preprocess_text(make_one_str(text_recognition(file))))

# TODO: Make it
@shared_task
def check_doc(achievement_id):
    achievement = Achievement.objects.get(pk=achievement_id)
    text = get_text_from_picture(achievement.picture.name)
    if (
        str(achievement.achievement.level)[:-2] in text
        and str(achievement.achievement.role)[:-2] in text
        and str(achievement.achievement.activity)[:-2] in text
        and str(achievement.user.first_name)[:-2] in text
        and str(achievement.user.last_name)[:-2] in text
    ):
        achievement.is_accepted = True
        achievement.save()


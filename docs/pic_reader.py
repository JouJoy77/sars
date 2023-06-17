import easyocr
import re
from pathlib import Path
import os

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
    img = open( os.path.join(BASE_DIR,'media','images', filename.split('/')[-1]),'rb')
    source = img.read()
    return reader.readtext(source, detail=0, paragraph=True)

def get_text_from_picture(file):
    return make_one_str(preprocess_text(make_one_str(text_recognition(file))))

def check_doc(achievement_id):
    from .models import Achievement
    achievement = Achievement.objects.get(pk=achievement_id)
    text = get_text_from_picture(achievement.picture.name)
    if (
        str(achievement.achievement.level.name).lower()[:-2] in text
        and str(achievement.achievement.role.name).lower()[:-2] in text
        and str(achievement.achievement.activity.name).lower()[:-2] in text
        and str(achievement.user.first_name).lower()[:-2] in text
        and str(achievement.user.last_name).lower()[:-2] in text
    ):
        achievement.is_accepted = True
        achievement.save()



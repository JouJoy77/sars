from django.shortcuts import render

from users.models import User

def index(request):
    users = User.objects.order_by('-points')
    table_data = [
        {'rank': rank, 'snils': user.snils, 'points': user.points}
        for rank, user in enumerate(users, start=1)
    ]
    context = {
        'Name': 'Главная страница',
        'table_data': table_data
    }

    return render(request, 'index.html', context)
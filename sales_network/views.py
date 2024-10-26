from django.shortcuts import render


def index(request):
    """ Главная страница сайта """
    return render(request, 'sales_network/index.html')

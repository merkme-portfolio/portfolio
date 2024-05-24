"""Модуль views приложения pages."""
from django.shortcuts import render


def page_not_found(request, exception):
    """
    Создаем кастомную функцию для вызова handler404.

    Прописана в urls проекта.
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """
    Создаем кастомную функцию для вызова handler404.

    Прописана в settings проекта
    """
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request, reason=''):
    """
    Создаем кастомную функцию для вызова handler500.

    Прописана в urls проекта
    """
    return render(request, 'pages/500.html', status=500)

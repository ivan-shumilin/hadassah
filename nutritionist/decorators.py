from django.contrib import messages
from django.shortcuts import redirect


def check_group_manager(user):
    return user.groups.filter(name='manager').exists()


def check_group_hadassah_report(user):
    return user.groups.filter(name='hadassah_report').exists()


def login_required_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or not check_group_manager(request.user):
            messages.info(request, "Для просмотра этой страницы нужно войти в систему как менеджер!")
            return redirect("login")
        else:
            return func(request, *args, **kwargs)
    return wrapper


def login_required_hadassah_report(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or not check_group_hadassah_report(request.user):
            messages.info(request, "У вас недостаточно прав просматривать эту страницу!")
            return redirect("login")
        else:
            return func(request, *args, **kwargs)
    return wrapper

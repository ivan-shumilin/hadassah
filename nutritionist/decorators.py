from django.contrib import messages
from django.shortcuts import redirect


def check_group_manager(user):
    return user.groups.filter(name="manager").exists()


def check_group_cafe(user):
    return user.groups.filter(name="cafe").exists()


def check_group_hadassah_report(user):
    return user.groups.filter(name="hadassah_report").exists()


def check_group_kitchen(user):
    return user.groups.filter(name="kitchen").exists()


def check_group_accountant(user):
    return user.groups.filter(name="accountant").exists()


def login_required_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or not check_group_manager(request.user):
            messages.info(
                request,
                "Для просмотра этой страницы нужно войти в систему как менеджер!",
            )
            return redirect("login")
        else:
            return func(request, *args, **kwargs)

    return wrapper


def login_required_hadassah_report(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or not check_group_hadassah_report(request.user):
            messages.info(
                request, "У вас недостаточно прав просматривать эту страницу!"
            )
            return redirect("login")
        else:
            return func(request, *args, **kwargs)

    return wrapper


def login_required_accountant(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or not check_group_accountant(request.user):
            messages.info(
                request,
                "Для просмотра этой страницы нужно войти в систему как бухгалтер-калькулятор!",
            )
            return redirect("login")
        else:
            return func(request, *args, **kwargs)

    return wrapper


def login_required_manager_and_kitchen(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or (
            not check_group_kitchen(request.user)
            and not check_group_manager(request.user)
        ):
            messages.info(
                request,
                "Для просмотра этой страницы нужно войти в систему как персонал кухни или менджер!",
            )
            return redirect("login")
        else:
            return func(request, *args, **kwargs)

    return wrapper


def login_required_cafe_and_kitchen_and_manager(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous or (
            not check_group_kitchen(request.user) and not check_group_cafe(request.user) and
            not check_group_manager(request.user)
        ):
            messages.info(
                request,
                "Для просмотра этой страницы нужно войти в систему как персонал кухни или повара кафе или менеджер!",
            )
            return redirect("login")
        else:
            return func(request, *args, **kwargs)

    return wrapper

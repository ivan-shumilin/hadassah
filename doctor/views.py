from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def group_doctors_check(user):
    return user.groups.filter(name='doctors').exists()


@login_required
@user_passes_test(group_doctors_check, login_url='login')
def doctor(request):
    return render(request, 'doctor.html', {})

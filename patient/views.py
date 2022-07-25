from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def group_patient_check(user):
    return user.groups.filter(name='patients').exists()


@login_required
@user_passes_test(group_patient_check, login_url='login')
def patient(request):
    return render(request, 'patient.html', {})


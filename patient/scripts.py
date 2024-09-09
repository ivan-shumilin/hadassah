from django.contrib.auth.models import Group
from django.db.models import Q
from nutritionist.models import CustomUser


def add_all_patients_to_group():
    """ добавляю всех пациентов (со статусами пациента и архивированного пациента) в группу пациент"""

    patients = CustomUser.objects.filter(Q(status='patient') | Q(status='patient_archive'))

    for patient in patients:
        group_patient = Group.objects.get(name='patients')
        group_patient.user_set.add(patient)

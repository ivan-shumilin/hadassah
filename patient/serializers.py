from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from nutritionist.models import CustomUser
from patient.functions import formating_name_for_login_patient


class CommentSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    rating = serializers.IntegerField()
    text = serializers.CharField()
    date = serializers.DateField(required=True)


class PatientLoginSerializer(serializers.Serializer):
    last_name = serializers.CharField()  # Фаммлия
    name = serializers.CharField()  # Имя
    patronymic = serializers.CharField()  # Отчество
    birth_date = serializers.DateField()

    def validate(self, data):
        last_name = data.get('last_name')
        name = data.get('name')
        patronymic = data.get('patronymic')
        birth_date = data.get('birth_date')

        # Аутентификация пользователя (проверка есть ли такой пользователь)
        try:
            formatted_full_name = formating_name_for_login_patient(name, last_name, patronymic)
            user = CustomUser.objects.get(full_name=formatted_full_name, birthdate=birth_date, status='patient')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": f"Patient {last_name} {name} {patronymic} does not exist or "
                                                         f"dont have status patient. "
                                              f"Invalid login credentials"})
        except CustomUser.MultipleObjectsReturned:
            raise serializers.ValidationError({"detail": f"Patient {last_name} {name} {patronymic} find more than one"})

        # Генерация access и refresh токенов для пользователя
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh = data.get('refresh')
        if not refresh:
            raise serializers.ValidationError({"detail": "Refresh token is required"})
        return data



from rest_framework import serializers

from doctor.functions.functions import add_features
from nutritionist.models import TimetableLp, CustomUser


class DishesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = TimetableLp
        fields = ('name', 'type_of_diet', 'id')

    def get_name(self, instance):
        return instance.item.name

    def get_id(self, instance):
        return instance.item.id

class PatientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('full_name', 'type_of_diet', 'id')

class InfoPatientSerializer(serializers.ModelSerializer):

    comment = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ('full_name', 'type_of_diet', 'comment')

    def get_comment(self, instance):
        comment = add_features(instance.comment,
                               instance.is_probe,
                               instance.is_without_salt,
                               instance.is_without_lactose,
                               instance.is_pureed_nutrition)
        return comment

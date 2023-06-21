from rest_framework import serializers

from doctor.functions.functions import add_features
from nutritionist.models import TimetableLp, CustomUser


class DishesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    class Meta:
        model = TimetableLp
        fields = ('name', 'type_of_diet', 'id', 'description')

    def get_name(self, instance):
        return instance.item.name

    def get_description(self, instance):
        return instance.item.description

    def get_id(self, instance):
        if self.context.get('type') == "cafe":
            return f'cafe-cat-{instance.item.id}'
        return instance.item.id

class PatientsSerializer(serializers.ModelSerializer):
    DIETS_COLORS_NAME = {
        'ОВД': {'name': 'ОВД', 'color': 'blue'},
        'ОВД б/с': {'name': 'ОВД б/с', 'color': 'mint'},
        'ОВД без сахара': {'name': 'ОВД б/с', 'color': 'blue'},
        'ОВД веган (пост) без глютена': {'name': 'ОВД веган', 'color': 'green'},
        'Нулевая диета': {'name': 'Нулевая диета', 'color': 'green'},
        'ЩД': {'name': 'ЩД', 'color': 'yellow'},
        'ЩД без сахара': {'name': 'ЩД без сахара', 'color': 'yellow'},
        'БД': {'name': 'БД', 'color': 'pink'},
        'БД день 1': {'name': 'БД день 1', 'color': 'pink'},
        'БД день 2': {'name': 'БД день 2', 'color': 'pink'},
        'ВБД': {'name': 'ВБД', 'color': 'orange'},
        'Без ограничений': {'name': 'Без ограничений', 'color': 'orange'},
        'НБД': {'name': 'НБД', 'color': 'red'},
        'НКД': {'name': 'НКД', 'color': 'red'},
        'ВКД': {'name': 'ВКД', 'color': 'purple'},
        'Безйодовая': {'name': 'Безйодовая', 'color': 'purple'},
        'ПЭТ/КТ': {'name': 'ПЭТ/КТ', 'color': 'pink'},
        }
    type_of_diet = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id',
                  'full_name',
                  'birthdate',
                  'receipt_date',
                  'receipt_time',
                  'floor',
                  'department',
                  'room_number',
                  'bed',
                  'type_of_diet',
                  'comment',
                  'extra_bouillon',
                  'color')

    def get_type_of_diet(self, instance):
        return self.DIETS_COLORS_NAME[instance.type_of_diet]['name']

    def get_color(self, instance):
        return self.DIETS_COLORS_NAME[instance.type_of_diet]['color']


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


class InputDataSerializer(serializers.Serializer):
    id_user = serializers.IntegerField()
    date_show = serializers.DateField()


class SendPatientProductsAPIViewSerializer(serializers.Serializer):
    id_user = serializers.CharField()
    date_show = serializers.CharField()
    products = serializers.CharField()
    meal = serializers.CharField()
    user_name = serializers.CharField()

class AddDishSerializer(serializers.Serializer):
    id_user = serializers.CharField()
    date = serializers.DateField()
    product_id = serializers.CharField()
    category = serializers.CharField()
    meal = serializers.CharField()


class ChangeDishSerializer(serializers.Serializer):
    id_user = serializers.IntegerField()
    date = serializers.DateField()
    product_id_add = serializers.CharField()
    product_id_del = serializers.CharField()
    category = serializers.CharField()
    meal = serializers.CharField()

class CroppImageSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    url = serializers.CharField()
    type = serializers.CharField()
from rest_framework import serializers

from nutritionist.models import TimetableLp, ProductLp


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
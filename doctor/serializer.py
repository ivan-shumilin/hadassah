from rest_framework import serializers

from nutritionist.models import TimetableLp, ProductLp


class DishesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = TimetableLp
        fields = ('name', 'type_of_diet')

    def get_name(self, instance):
        return instance.item.name
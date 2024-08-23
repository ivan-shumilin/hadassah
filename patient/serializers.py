from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    rating = serializers.IntegerField()
    text = serializers.CharField()
    date = serializers.DateField(required=True)

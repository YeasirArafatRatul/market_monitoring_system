from rest_framework import serializers
from lenden.models import Chalan


class ChalanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chalan
        fields = ('price',)

from rest_framework import serializers
from lenden.models import Chalan,SellProduct


class ChalanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellProduct
        fields = ('price',)


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellProduct
        fields = ('price',)
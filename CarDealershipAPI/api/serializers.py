from rest_framework import serializers

from .models import *

class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name']

class CarModelSerializer(serializers.ModelSerializer):
    carMake = serializers.StringRelatedField()
    class Meta:
        model = CarModel
        fields = ['name', 'carMake']

class CarSerializer(serializers.ModelSerializer):
    carModel = CarModelSerializer()
    engineType = serializers.StringRelatedField()
    condition = serializers.StringRelatedField()
    color = serializers.StringRelatedField()
    class Meta:
        model = Car
        fields = ['id', 'carModel', 'year', 'milage', 'engineType', 'condition', 'color', 'img']
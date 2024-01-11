from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    temp = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    pressure_mm = serializers.IntegerField()

from rest_framework import serializers
from .models import CarMark, CarModel, Offer, Request


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name', 'country']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'car_mark_id', 'name', 'model_class', 'year_from', 'year_to']


class RequestSerializer(serializers.ModelSerializer):
    car_mark = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    car_model = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Request
        fields = ['id', 'car_mark', 'car_model', 'color', 'additional_requirements']


class OfferSerializer(serializers.ModelSerializer):
    car_mark = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    car_model = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Offer
        fields = ['id', 'car_mark', 'car_model', 'color', 'mileage', 'year_of_issue', 'additional_properties']

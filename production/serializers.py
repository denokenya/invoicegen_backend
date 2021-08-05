from rest_framework import serializers
from production.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = RecipeIngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = "__all__"
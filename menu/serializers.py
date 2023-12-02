from rest_framework import serializers
from .models import Category, FoodItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'image_url', 'description', "price", "category",)
        read_only_fields = ('id',)
        depth = 1
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from myapp.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data
class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name','description','active', 'category']


from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from myapp.models import Category, Product

class CategoryListSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']
 
    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value
 
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data
class CategoryDetailSerializer(serializers.ModelSerializer):
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


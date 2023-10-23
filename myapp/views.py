from rest_framework.views import APIView
from rest_framework.response import Response

from myapp.models import Category, Product
from myapp.serializers import CategorySerializer, ProductSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
 

 
class CategoryViewset(ReadOnlyModelViewSet):
 
    serializer_class = CategorySerializer
 
    def get_queryset(self):
        return Category.objects.filter(active=True)
class ProductViewset(ReadOnlyModelViewSet):
 
    serializer_class = ProductSerializer
 
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class CategoryView(APIView):

    def get(self, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):

    def get(self, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from myapp.models import Category, Product
from myapp.serializers import CategoryDetailSerializer,CategoryListSerializer, ProductSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from myapp.permissions import IsAdminAuthenticated
class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class() 


 
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminAuthenticated]
 
    def get_queryset(self):
        return Category.objects.all()

class CategoryViewset(ReadOnlyModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.filter(active=True)
 
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        category = self.get_object()
        category.active = False
        category.save()

        # Puis désactivons les produits de cette catégorie
        category.products.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()
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
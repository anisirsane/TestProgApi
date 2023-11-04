from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from myapp.views import CategoryViewset,ProductViewset,AdminCategoryViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)), # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import action


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().disable()
        return Response()

class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('myapp.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('myapp.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name 
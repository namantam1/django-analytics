from django.shortcuts import render

from rest_framework import serializers

from .models import Product
from analytics.mixin import ObjectViewMixin, analytics_view_decorator

# Create your views here.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductDetail(ObjectViewMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # @analytics_view_decorator
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
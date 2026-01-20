
from apps.products.models.product_model import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'category_name', 'premium', 'stock', 'description', "rating_avg", "rating_count",]
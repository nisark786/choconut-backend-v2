from rest_framework import serializers
from apps.products.models.product_model import Product

class AdminProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Product.objects.values_list("category", flat=True),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "category_id",
            "category_name",
            "premium",
            "stock",
            "description",
            "rating_avg",
            "rating_count",
        ]
        read_only_fields = ["id","rating_avg", "rating_count", "category_name"]

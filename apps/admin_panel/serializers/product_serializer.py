from apps.products.models.category_model import Category
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



class AdminProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "image",
            "category",
            "premium",
            "stock",
            "description",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_category(self, value):
        try:
            return Category.objects.get(name=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Invalid category.")

    def create(self, validated_data):
        category = validated_data.pop("category")

        product = Product.objects.create(
            category=category,
            rating_avg=0,
            rating_count=0,
            **validated_data
        )
        return product
    
    


class AdminProductUpdateSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "image",
            "category",
            "premium",
            "stock",
            "description",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_category(self, value):
        try:
            return Category.objects.get(name=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Invalid category.")

    def update(self, instance, validated_data):
        category = validated_data.pop("category")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.category = category
        instance.save()

        return instance

from apps.products.models.category_model import Category
from rest_framework import serializers
from apps.products.models.product_model import Product
from ..tasks import upload_product_image_task

class AdminProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "price", "image", "category_name",
            "premium", "stock", "description", "rating_avg", "rating_count",
        ]
        read_only_fields = ["id", "rating_avg", "rating_count", "category_name"]

class AdminProductCreateSerializer(serializers.ModelSerializer):
    # This automatically converts the string (e.g., "Chocolates") into a Category object
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=True
    )

    class Meta:
        model = Product
        fields = ["name", "price", "image", "category", "premium", "stock", "description"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def create(self, validated_data):
        image_url = validated_data.get("image")

        product = Product.objects.create(
            rating_avg=0,
            rating_count=0,
            **validated_data # validated_data['category'] is already the object
        )

        # Offload the "Artisanal" compression to Celery
        if image_url:
            upload_product_image_task.delay(product.id, image_url)

        return product

class AdminProductUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False # Allow partial updates
    )

    class Meta:
        model = Product
        fields = ["name", "price", "image", "category", "premium", "stock", "description"]

    def update(self, instance, validated_data):
        image_url = validated_data.get("image")
        
        # Check if the image changed before popping it
        image_changed = image_url and image_url != instance.image

        # Update all fields including 'category' object
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Trigger Celery only if a new visual asset was provided
        if image_changed:
            upload_product_image_task.delay(instance.id, image_url)

        return instance
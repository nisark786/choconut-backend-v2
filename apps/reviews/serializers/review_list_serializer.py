from rest_framework import serializers
from apps.reviews.models.review_model import Review


class ReviewListSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source="user.name", read_only=True)
    date = serializers.DateTimeField(source="created_at", read_only=True,format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Review
        fields = [
            "id",
            "userName",
            "rating",
            "title",
            "comment",
            "recommend",
            "verified",
            "date",
        ]

from rest_framework import serializers

from app.models import Entity, Category, Icon


class EntitySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.friendly_name')
    category_id = serializers.ReadOnlyField(source='category.id')

    class Meta:
        model = Entity
        fields = [
            "id",
            "entity_id",
            "entity_type",
            "image",
            "title",
            "description",
            "category_name",
            "category_id",
            "subscribers"
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "friendly_name", "app_icon_id"]


class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = ["id", "alias"]

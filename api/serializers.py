from rest_framework.serializers import ModelSerializer
from shelter.models import Animals


class AnimalsViewSerializer(ModelSerializer):
    class Meta:
        model = Animals
        exclude = ['is_deleted', 'deleted_at']


class AnimalsEditSerializer(ModelSerializer):
    class Meta:
        model = Animals
        exclude = ['created_at', 'modified_at', 'is_deleted', 'deleted_at']

from django.forms import ModelForm
from .models import Animals


class AnimalsForm(ModelForm):
    class Meta:
        model = Animals
        exclude = ['created_at', 'modified_at', 'is_deleted', 'deleted_at']


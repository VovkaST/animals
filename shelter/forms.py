from django.forms import ModelForm
from .models import Animals


class AnimalsViewForm(ModelForm):
    class Meta:
        model = Animals
        fields = '__all__'


class AnimalsEditForm(ModelForm):
    class Meta:
        model = Animals
        exclude = ['created_at', 'modified_at']

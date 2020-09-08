from django.forms import ModelForm, Textarea

from .models import Animals


class AnimalsForm(ModelForm):
    class Meta:
        model = Animals
        exclude = ['shelter', 'created_at', 'modified_at', 'is_deleted', 'deleted_at']
        widgets = {
            'special_signs': Textarea(attrs={'rows': 3, 'cols': 50})
        }

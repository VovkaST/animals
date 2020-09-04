from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Animals
from datetime import datetime


class AnimalsForm(ModelForm):
    class Meta:
        model = Animals
        exclude = ['created_at', 'modified_at', 'is_deleted', 'deleted_at']

    def gt_current_date(self, date_field, error_msg):
        field_value = self.cleaned_data[date_field]
        if field_value > datetime.now().date():
            raise ValidationError(error_msg)
        return field_value

    def clean_birth_date(self):
        try:
            return self.gt_current_date(date_field='birth_date',
                                        error_msg='Дата рождения не может быть больше текущей')
        except ValidationError:
            raise

    def clean_arrive_date(self):
        try:
            return self.gt_current_date(date_field='arrive_date',
                                        error_msg='Дата прибытия не может быть больше текущей')
        except ValidationError:
            raise

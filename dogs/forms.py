import datetime

from crispy_forms.layout import Submit
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dogs.models import Dog


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class DogForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Dog
        fields = '__all__'

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        current_year = datetime.datetime.now().year
        print(current_year)
        print(cleaned_data.year)
        if current_year - cleaned_data.year > 100:
            raise forms.ValidationError('Собака должна быть моложе 100 лет')

        return cleaned_data


class ParentForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Dog
        fields = '__all__'





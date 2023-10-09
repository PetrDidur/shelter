from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class StyleUserRegisterFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))


class UserRegisterForm(StyleUserRegisterFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'tg_nick', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()



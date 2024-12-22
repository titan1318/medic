from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, (forms.BooleanField, forms.ModelMultipleChoiceField)):
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')


class LoginForm(StyleFormMixin, AuthenticationForm):

    class Meta:
        model = User
        fields = ('email', 'password')


class UserForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'phone', 'address', 'photo', 'comment',)

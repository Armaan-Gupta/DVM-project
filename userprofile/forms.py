from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_vendor = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')

        # Handle the case when the checkbox is not selected
        if is_vendor is False or is_vendor is None:
            # Set a default value for the boolean field or handle the error as needed
            cleaned_data['is_vendor'] = False

        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_vendor',]
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_vendor = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')

        if is_vendor is False or is_vendor is None:
            cleaned_data['is_vendor'] = False

        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_vendor',]

class AddAmountForm(forms.ModelForm):
    wallet = forms.IntegerField()

    class Meta:
        model = User
        fields = ['wallet']



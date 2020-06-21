from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=2)
    password = forms.CharField(required=True, max_length=3)

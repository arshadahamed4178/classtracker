from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Email"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-input",
                "placeholder": "Create Password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-input",
                "placeholder": "Confirm Password"
            }),
        }
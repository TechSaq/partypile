from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

from .models import AuthUser


class CreateAuthUserForm(forms.Form):
    username = forms.CharField(label="Username", min_length=6, max_length=150)
    first_name = forms.CharField(label="First Name", min_length=2, max_length=150)
    last_name = forms.CharField(label="Last Name", min_length=2, max_length=150)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"id": "password1"})
    )
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(attrs={"id": "password2"})
    )
    phone = forms.CharField(label="Phone", max_length=15, required=False)

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        user.save()

        authUser = AuthUser.objects.create(
            user=user,
            phone=self.cleaned_data["phone"],
        )

        return authUser

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Category


class CreateUserForm(UserCreationForm):
    """Create User"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with the same name already exists")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
            self.fields[field].help_text = ""
            self.fields[field].label = ""
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"
        self.fields["email"].widget.attrs["placeholder"] = "Email"


class LoginUserForm(AuthenticationForm):
    """Login Form"""
    username = forms.CharField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs["class"] = "form-control"
            self.fields[filed].widget.attrs["placeholder"] = self.fields[filed].label
            self.fields[filed].label = ""


class CategoryForm(forms.ModelForm):
    """Category Form"""

    class Meta:
        model = Category
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["placeholder"] = "Name of category"
        self.fields["title"].label = ""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Blog, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "description", "body", "image", "category"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "body": forms.Textarea(attrs={"rows": 10}),
            "image": forms.ClearableFileInput(attrs={"multiple": False}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Поле 'Заголовок' не может быть пустым.")
        return title

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if not body:
            raise forms.ValidationError("Поле 'Содержимое' не может быть пустым.")
        return body

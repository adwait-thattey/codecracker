from django import forms

from registration import models

from django.core.validators import MinLengthValidator


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[MinLengthValidator(8)])
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.DefaultUser
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if models.DefaultUser.objects.filter(username=username).exists():
            self.add_error("username", "This username already exists. Please choose another")

        elif models.DefaultUser.objects.filter(email=email).exists():
            self.add_error("email", "A user with this email already exists. Please login to your account")

        elif password != confirm_password:
            self.add_error("confirm_password", "Both Passwords Do Not Match!")

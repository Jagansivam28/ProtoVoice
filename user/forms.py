from django import forms
from validate_email import validate_email
from django.contrib.auth import get_user_model
from .models import User

class UserRegisterationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    password=forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        exclude = ['date_joined', 'username','dob',"last_name"]



    def save(self):
        data = self.cleaned_data
        user = User.objects.create(username=data['email'], email=data['email'], is_active=True,
                                   first_name=data['first_name'])
        return user

    def update(self,user):
        data = self.cleaned_data
        user.first_name=data['first_name']
        user.save()
        return user


class UserLoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields=['email']



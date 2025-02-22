from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserInfo
class UserRegisterForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'your email'}))
    password=forms.CharField(label='Enter ur password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}))
    password2 = forms.CharField(label='confirm ur password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password'}))
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email address has already registered')
        return email

    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username has already registered, you might want to loggin or change ur username')
        return username

    def clean(self):
        cd=super().clean()
        p1=cd.get('password')
        p2=cd.get('password2')

        if p1 and p2 and p1 != p2 :
            raise ValidationError('passwords do not match')



class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}))


class UserProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter a valid username'}))


class UserEditForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model = UserInfo
        fields=['age','bio','email']













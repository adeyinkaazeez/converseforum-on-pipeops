from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from business.models import Business, Business_Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)
    

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
        username = forms.CharField(widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
                                     label="Username or Email*")
    
        password = forms.CharField(widget=forms.PasswordInput)



class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
    
    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                                                       .filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data

class ProfileEditForm(forms.ModelForm):
    date_of_birth= forms.DateField(widget = forms.SelectDateWidget())
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'about', 'location', 'photo']
        widgets = {'date_of_birth':forms.DateInput(format=('%m/%d/%y'), attrs={'class':'form-control', 'placeholder':'Select your birth date', 'type':'date'}),}

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


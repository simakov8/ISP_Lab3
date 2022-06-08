import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def confirm_login_allowed(self, user):
        if self.request.user.is_authenticated:
            raise ValidationError(
                'Для входа в акканут сначала выйдете из текущего аккаунта',
            )


class AddToCartForm(forms.Form):
    count = forms.IntegerField(label='Количество', min_value=1, widget=forms.NumberInput())


class MakeOrderForm(forms.Form):
    firstname = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Phone No', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = [
            'firstname',
            'lastname',
            'address',
            'phone',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            return email
        else:
            raise forms.ValidationError("Invalid email")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if re.match(r"[\d]{2} [\d]{2} [\d]{2} [\d]{3}", phone):
            return phone
        else:
            raise forms.ValidationError("Phone should be like this : 29 12 34 567")

    def clean_firstname(self):
        firstname = self.cleaned_data['firstname']
        if re.search(r'^[A-z][A-z|\.|\s]+$', firstname) is None:
            raise forms.ValidationError("Wrong name")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        if re.search(r'^[A-z][A-z|\.|\s]+$', lastname) is None:
            raise forms.ValidationError("Wrong lastname")
        return lastname

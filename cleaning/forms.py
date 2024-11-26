from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Users, Order
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    login = forms.CharField(label='Имя пользователя')
    email = forms.CharField(label='Эллектронная почта')
    full_name = forms.CharField(label='ФИО')
    phone = forms.CharField(label='Номер телефона')
    
    class Meta:
        model = Users
        fields = ['login', 'email', 'full_name', 'password1', 'password2', 'phone']

class UserLoginForm(forms.ModelForm):
    login = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['login', 'password']

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        if login and password:
            user = authenticate(login=login, password=password)
            if not user:
                raise forms.ValidationError('Неправильный логин или пароль.')
        return self.cleaned_data

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'contact_data', 'service_id', 'payment_type', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad
from .models import Contact
from .models import Profile
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone_number = forms.CharField(max_length=30, required=True, label='Номер телефона')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput, label='Повторите пароль')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.last_name = self.cleaned_data['last_name']
        phone_number = self.cleaned_data['phone_number']
        user.set_password(self.cleaned_data['password1'])
        user.save()

        return user
    class Meta:
        model = User
        fields = ('username', 'last_name', 'phone_number', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }



class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['photo', 'title', 'category', 'description', 'location', 'price', 'phone_number']
        labels = {'title': 'Название товара', 'category': 'Выбор категории', 'description': 'Описание товара', 'price': 'Цена товара', 'location': 'Местоположение', 'phone_number': 'Номер телефона', 'photo': 'Фотографии'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        ad = super().save(commit=False)
        if self.request:
            ad.user = self.request.user
        if commit:
            ad.save()
        return ad
# class AdForm(forms.ModelForm):
#     class Meta:
#         model = Ad
#         fields = ['photo', 'title', 'category', 'description', 'location', 'price', 'phone_number']
#         labels = {'title': 'Название товара', 'category': 'Выбор категории', 'description': 'Описание товара', 'price': 'Цена товара', 'location': 'Местоположение', 'phone_number': 'Номер телефона', 'photo': 'Фотографии'}
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-select'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control'}),
#             'location': forms.Select(attrs={'class': 'form-select'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']


class AdFilterForm(forms.Form):
    title = forms.CharField(label='Поиск по названию', required=False)
    # category = forms.ModelChoiceField(label='Категория',queryset=Ad.objects.values_list('category', flat=True).distinct(), required=False)
    price_min = forms.DecimalField(label='Минимальная цена', required=False)
    price_max = forms.DecimalField(label='Максимальная цена', required=False)
    location = forms.ChoiceField(label='Регион', choices=Ad.LOCATION_CHOICES, required=False)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad
from .models import Contact
from .models import Profile
from .models import Message
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from .models import MessageEmail
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
    username = forms.CharField(max_length=30, required=True, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'register-input'}))

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
            'photo': forms.ClearableFileInput(attrs={'class': 'form-controlph'}),
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

class TitleSearchForm(forms.Form):
    simple_title = forms.CharField(label='Поиск ', required=False)

class MainFilter(forms.Form):
    title = forms.CharField(label='Поиск по названию', required=False)

class MessageFormEmail(forms.Form):
    name = forms.CharField(max_length=100, label="Как к Вам обращаться")
    email = forms.EmailField(label="Ваша почта")
    message = forms.CharField(widget=forms.Textarea, label="Опишите проблему")

    def send_email_support(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        subject = 'Question from {}'.format(name)
        message = 'From: {}\n\n{}'.format(email, message)
        from_email = 'testdjangosmeta@mail.ru'
        recipient_list = ['testdjangosmeta@mail.ru']
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Ad(models.Model):
    CATEGORY_CHOICES = (
        ('обувь', 'обувь'),
        ('одежда', 'одежда'),
        ('мебель', 'мебель'),
        ('автомобиль', 'автомобиль'),
        ('квартира', 'квартира'),
        ('игрушки', 'игрушки'),
        ('развлечения', 'развлечения'),
    )

    LOCATION_CHOICES = (
        ('MT', 'Минская область'),
        ('BR', 'Брестская область'),
        ('VG', 'Витебская область'),
        ('HO', 'Гомельская область'),
        ('GR', 'Гродненская область'),
        ('MO', 'Могилевская область'),
        ('MN', 'Минск'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) # добавлено поле для ссылки на пользователя
    title = models.CharField(max_length=100, default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='category1')
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=50, default='MT')
    phone_number = models.CharField(max_length=20, default='')
    photo = models.ImageField('Изображение', upload_to='postads/', default='postads/default.jpg')

    def __str__(self):
        return self.title
# class Ad(models.Model):
#     CATEGORY_CHOICES = (
#         ('обувь', 'обувь'),
#         ('одежда', 'одежда'),
#         ('мебель', 'мебель'),
#         ('автомобиль', 'автомобиль'),
#         ('квартира', 'квартира'),
#         ('игрушки', 'игрушки'),
#         ('развлечения', 'развлечения'),
#     )
#
#     LOCATION_CHOICES = (
#         ('MT', 'Минская область'),
#         ('BR', 'Брестская область'),
#         ('VG', 'Витебская область'),
#         ('HO', 'Гомельская область'),
#         ('GR', 'Гродненская область'),
#         ('MO', 'Могилевская область'),
#         ('MN', 'Минск'),
#     )
#
#     title = models.CharField(max_length=100, default='')
#     category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='category1')
#     description = models.TextField(default='')
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     location = models.CharField(choices=LOCATION_CHOICES, max_length=50, default='MT')
#     phone_number = models.CharField(max_length=20, default='')
#     photo = models.ImageField('Изображение', upload_to='postads/', default='postads/default.jpg')
#
#     def __str__(self):
#         return self.title


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class UserAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.ad.title}"

class Order(models.Model):
    email = models.EmailField()

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)  # Создаем профиль пользователя при создании нового пользователя
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
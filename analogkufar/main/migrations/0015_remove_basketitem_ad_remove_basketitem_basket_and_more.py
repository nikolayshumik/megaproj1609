# Generated by Django 4.2 on 2023-08-15 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_basket_basketitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketitem',
            name='ad',
        ),
        migrations.RemoveField(
            model_name='basketitem',
            name='basket',
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
        migrations.DeleteModel(
            name='BasketItem',
        ),
    ]
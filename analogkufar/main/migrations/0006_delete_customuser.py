# Generated by Django 4.2 on 2023-08-13 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
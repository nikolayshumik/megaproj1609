# Generated by Django 4.1.11 on 2023-09-08 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_remove_message_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=20)),
            ],
        ),
    ]
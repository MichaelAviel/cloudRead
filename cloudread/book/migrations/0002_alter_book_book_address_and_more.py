# Generated by Django 4.0.4 on 2022-07-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_address',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='secret_access_code',
            field=models.CharField(blank=True, default='', max_length=400, null=True),
        ),
    ]

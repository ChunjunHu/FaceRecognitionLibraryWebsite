# Generated by Django 2.0.1 on 2019-01-11 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0016_auto_20190111_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='getdatacss',
            name='copyBook',
        ),
    ]
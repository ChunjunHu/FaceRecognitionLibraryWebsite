# Generated by Django 2.0.1 on 2019-01-13 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0037_register_borrowtimes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerCss',
        ),
        migrations.DeleteModel(
            name='CustomerHtml',
        ),
        migrations.DeleteModel(
            name='CustomerJavaScript',
        ),
    ]

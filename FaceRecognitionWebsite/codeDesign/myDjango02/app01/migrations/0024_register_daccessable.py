# Generated by Django 2.0.1 on 2019-01-13 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0023_register_dqrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='daccessable',
            field=models.IntegerField(default=1),
        ),
    ]

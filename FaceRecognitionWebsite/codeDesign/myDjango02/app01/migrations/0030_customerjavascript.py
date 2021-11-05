# Generated by Django 2.0.1 on 2019-01-13 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0029_delete_customerjavascript'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerJavaScript',
            fields=[
                ('Jsid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('imgUrl', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=200)),
                ('fee', models.IntegerField(default=0)),
                ('borrowTime', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
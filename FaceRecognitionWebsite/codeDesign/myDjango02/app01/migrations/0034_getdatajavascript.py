# Generated by Django 2.0.1 on 2019-01-13 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0033_delete_getdatajavascript'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetDataJavaScript',
            fields=[
                ('Jsid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('imgUrl', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=200)),
                ('copyBook', models.IntegerField(default=1)),
            ],
        ),
    ]

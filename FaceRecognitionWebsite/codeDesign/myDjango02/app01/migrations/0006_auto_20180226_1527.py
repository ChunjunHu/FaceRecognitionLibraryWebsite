# Generated by Django 2.0.1 on 2018-02-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20180226_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getdatacss',
            name='Jsid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='getdatacss',
            name='details',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='getdatacss',
            name='imgUrl',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='getdatacss',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
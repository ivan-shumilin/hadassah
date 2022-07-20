# Generated by Django 4.0.6 on 2022-07-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutritionist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='comment',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='not_suitable',
            field=models.BooleanField(null=True),
        ),
    ]

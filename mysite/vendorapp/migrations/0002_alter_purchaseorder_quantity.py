# Generated by Django 5.0 on 2023-12-07 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]

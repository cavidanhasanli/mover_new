# Generated by Django 2.0.1 on 2019-03-12 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping_app', '0020_productitem_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttag',
            name='name',
            field=models.CharField(default='Product_', max_length=500),
        ),
    ]

# Generated by Django 2.0.1 on 2019-03-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping_app', '0018_auto_20190311_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttag',
            name='name',
            field=models.CharField(default='Product_', max_length=50),
        ),
    ]
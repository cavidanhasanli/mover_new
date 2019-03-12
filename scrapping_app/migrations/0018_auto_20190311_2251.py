# Generated by Django 2.0.1 on 2019-03-11 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping_app', '0017_producttag_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='color',
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='image',
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='price',
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='size',
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='url',
        ),
        migrations.AddField(
            model_name='productitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapping_app.ProductTag'),
        ),
    ]

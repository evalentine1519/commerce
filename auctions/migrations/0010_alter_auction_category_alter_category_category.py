# Generated by Django 4.0.3 on 2022-04-19 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('1', 'misc'), ('art', 'art'), ('electronics', 'electronics'), ('auto', 'auto'), ('toys', 'toys'), ('books', 'books'), ('clothing', 'clothing')], default='misc', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(choices=[('1', 'misc'), ('art', 'art'), ('electronics', 'electronics'), ('auto', 'auto'), ('toys', 'toys'), ('books', 'books'), ('clothing', 'clothing')], default='misc', max_length=11),
        ),
    ]

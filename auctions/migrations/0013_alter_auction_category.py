# Generated by Django 4.0.3 on 2022-04-20 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_category_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(limit_choices_to=[(1, 'Misc'), (2, 'Art'), (3, 'Electronics'), (4, 'Auto'), (5, 'Toys'), (6, 'Books'), (7, 'Clothing')], null=True, on_delete=django.db.models.deletion.SET_NULL, to='auctions.category'),
        ),
    ]
# Generated by Django 3.0.3 on 2020-05-12 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0019_auto_20200510_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]

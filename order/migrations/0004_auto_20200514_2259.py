# Generated by Django 3.0.3 on 2020-05-14 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200514_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preaparing', 'Preaparing'), ('OnShipping', 'OnShipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=20),
        ),
    ]
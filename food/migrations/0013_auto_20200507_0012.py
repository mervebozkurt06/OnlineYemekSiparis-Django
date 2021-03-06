# Generated by Django 3.0.3 on 2020-05-06 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_auto_20200507_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='keywords',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-22 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0005_alter_art_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]

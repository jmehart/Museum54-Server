# Generated by Django 4.0.4 on 2022-06-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='classification',
            field=models.ManyToManyField(related_name='artclassification', to='app_api.classification'),
        ),
    ]

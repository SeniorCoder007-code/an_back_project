# Generated by Django 2.2.3 on 2020-05-09 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='cronical',
            field=models.CharField(default='', max_length=500),
        ),
    ]
# Generated by Django 2.2.3 on 2019-11-28 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixer', '0005_errors_proc'),
    ]

    operations = [
        migrations.AddField(
            model_name='mix',
            name='validated_winner',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 2.2.3 on 2019-12-12 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixer', '0007_mix_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='mix',
            name='initial_deposit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='txid',
            field=models.CharField(default='not sent yet', max_length=5000),
        ),
    ]

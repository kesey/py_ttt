# Generated by Django 4.2 on 2023-04-26 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttt_front', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cassette',
            name='nombre_exemplaire',
            field=models.IntegerField(blank=True, default=75, null=True),
        ),
        migrations.AlterField(
            model_name='cassette',
            name='prix',
            field=models.DecimalField(blank=True, decimal_places=2, default=6.0, max_digits=4, null=True),
        ),
    ]
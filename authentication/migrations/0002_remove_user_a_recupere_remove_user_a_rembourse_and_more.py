# Generated by Django 4.2 on 2023-04-22 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='a_recupere',
        ),
        migrations.RemoveField(
            model_name='user',
            name='a_rembourse',
        ),
        migrations.RemoveField(
            model_name='user',
            name='suppr',
        ),
        migrations.CreateModel(
            name='ComptaVendeur',
            fields=[
                ('id_compta_vendeur', models.AutoField(primary_key=True, serialize=False)),
                ('a_rembourse', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('a_recupere', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('id_vendeur', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'compta_vendeur',
            },
        ),
    ]

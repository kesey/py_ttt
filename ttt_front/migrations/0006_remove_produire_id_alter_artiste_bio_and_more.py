# Generated by Django 4.2 on 2023-04-17 21:49

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ttt_front', '0005_remove_produire_id_alter_produire_id_artiste_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artiste',
            name='bio',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cassette',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description_event',
            field=tinymce.models.HTMLField(blank=True, null=True),
        )
    ]
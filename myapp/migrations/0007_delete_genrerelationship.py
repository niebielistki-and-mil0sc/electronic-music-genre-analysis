# Generated by Django 5.0.3 on 2024-03-20 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_genreinfo_active_end_year_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GenreRelationship',
        ),
    ]

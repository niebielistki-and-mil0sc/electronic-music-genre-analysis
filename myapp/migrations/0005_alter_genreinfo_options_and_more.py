# Generated by Django 5.0.3 on 2024-03-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_genreinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genreinfo',
            options={'verbose_name': 'Genre Info', 'verbose_name_plural': 'Genre Info'},
        ),
        migrations.RemoveField(
            model_name='genreinfo',
            name='parent_genre',
        ),
        migrations.AddField(
            model_name='genreinfo',
            name='parent_genres',
            field=models.ManyToManyField(blank=True, help_text='The parent genre from which this genre arose.', related_name='derived_genres', to='myapp.genreinfo'),
        ),
    ]

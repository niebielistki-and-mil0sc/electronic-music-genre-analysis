# Generated by Django 5.0.3 on 2024-03-20 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_genreinfo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genreinfo',
            name='active_end_year',
            field=models.IntegerField(blank=True, help_text="The year when the genre's initial active period ended or the current year if it's ongoing.", null=True),
        ),
        migrations.AddField(
            model_name='genreinfo',
            name='active_start_year',
            field=models.IntegerField(blank=True, help_text='The year when the genre became distinctively active.', null=True),
        ),
        migrations.AddField(
            model_name='genreinfo',
            name='formation_end_year',
            field=models.IntegerField(blank=True, help_text="The year when the genre's formation was essentially complete.", null=True),
        ),
        migrations.AddField(
            model_name='genreinfo',
            name='formation_start_year',
            field=models.IntegerField(blank=True, help_text='The year when the genre began forming.', null=True),
        ),
    ]
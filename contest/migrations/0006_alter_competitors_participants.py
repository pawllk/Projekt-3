# Generated by Django 4.0.5 on 2022-06-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_alter_tournament_player_alter_tournament_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitors',
            name='participants',
            field=models.ManyToManyField(to='contest.player'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-10-20 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_buzzer_problem_buzzers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='buzzer',
            new_name='buzzers',
        ),
    ]
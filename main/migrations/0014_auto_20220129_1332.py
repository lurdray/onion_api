# Generated by Django 3.1.7 on 2022-01-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20220129_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='video',
            field=models.FileField(blank=True, default='default_files/default_video.mp4', upload_to='account_files/videos/'),
        ),
    ]
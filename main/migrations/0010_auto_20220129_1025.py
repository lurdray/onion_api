# Generated by Django 3.1.7 on 2022-01-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20220129_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='video',
            field=models.FileField(blank=True, default='default_files/default.mp4', upload_to='4app_files/videos/Sapp_files/videos/0app_files/videos/Oapp_files/videos/Mapp_files/videos/5app_files/videos/Tapp_files/videos/Papp_files/videos/9app_files/videos/W'),
        ),
    ]
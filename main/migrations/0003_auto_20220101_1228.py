# Generated by Django 3.1.7 on 2022-01-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220101_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='video',
            field=models.FileField(blank=True, default='default_files/default.mp4', upload_to='0app_files/videos/Japp_files/videos/Vapp_files/videos/Wapp_files/videos/Lapp_files/videos/Gapp_files/videos/Rapp_files/videos/Capp_files/videos/Xapp_files/videos/6'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='video',
            field=models.FileField(blank=True, default='default_files/default.mp4', upload_to='3app_files/videos/Iapp_files/videos/Xapp_files/videos/Sapp_files/videos/Yapp_files/videos/Kapp_files/videos/Wapp_files/videos/Rapp_files/videos/Tapp_files/videos/M'),
        ),
    ]
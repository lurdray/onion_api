# Generated by Django 3.1.7 on 2022-01-02 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20220102_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='video',
            field=models.FileField(blank=True, default='default_files/default.mp4', upload_to='Fapp_files/videos/Sapp_files/videos/3app_files/videos/Tapp_files/videos/Aapp_files/videos/Bapp_files/videos/Japp_files/videos/Uapp_files/videos/Sapp_files/videos/4'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='video',
            field=models.FileField(blank=True, default='default_files/default.mp4', upload_to='1app_files/videos/Rapp_files/videos/Oapp_files/videos/5app_files/videos/Zapp_files/videos/Aapp_files/videos/Napp_files/videos/Sapp_files/videos/3app_files/videos/6'),
        ),
    ]
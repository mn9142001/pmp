# Generated by Django 4.2.2 on 2023-07-05 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_customuser_is_active_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_login',
        ),
        migrations.AddField(
            model_name='course',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='Courses_trailer_videos/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
    ]
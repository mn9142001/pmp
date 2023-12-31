# Generated by Django 4.2.2 on 2023-07-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_remove_customuser_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images'),
        ),
        migrations.AlterField(
            model_name='course',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to='Courses_trailer_videos'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='lesson_pdfs'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='lesson_videos'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopseeapp', '0007_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='userprofile.png', null=True, upload_to='users/'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-11 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopseeapp', '0006_alter_profile_bio_alter_profile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='static/img/userprofile.png', null=True, upload_to='users/'),
        ),
    ]

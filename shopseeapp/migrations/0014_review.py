# Generated by Django 5.0.2 on 2024-02-12 11:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopseeapp', '0013_order_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Desc', models.TextField(max_length=1000)),
                ('rate', models.PositiveSmallIntegerField()),
                ('email', models.EmailField(max_length=100, null=True)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopseeapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

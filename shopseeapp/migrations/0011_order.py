# Generated by Django 5.0.2 on 2024-02-11 15:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopseeapp', '0010_profile_pincode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('phonenumber', models.IntegerField()),
                ('ordernotes', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=200)),
                ('orderid', models.CharField(default=None, max_length=100, null=True, unique=True)),
                ('payment_status', models.CharField(default='Failure', max_length=254, verbose_name='payment_choices')),
                ('processing_status', models.CharField(default='Pending', max_length=100, null=True)),
                ('razorpay_order_id', models.CharField(max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200)),
                ('razorpay_signature', models.CharField(blank=True, max_length=200)),
                ('datetime_of_payment', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

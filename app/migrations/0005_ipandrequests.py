# Generated by Django 4.1.1 on 2022-09-20 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_bid_bid_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPandRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.TextField(verbose_name='IP Address')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Created At')),
            ],
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-19 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_followers'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='event',
            table='event',
        ),
        migrations.AlterModelTable(
            name='eventimage',
            table='event_image',
        ),
    ]

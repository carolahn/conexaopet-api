# Generated by Django 5.0.3 on 2024-03-16 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cupom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupom',
            name='description',
            field=models.TextField(null=True),
        ),
    ]

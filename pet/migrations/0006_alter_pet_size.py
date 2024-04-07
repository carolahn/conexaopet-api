# Generated by Django 5.0.3 on 2024-03-29 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0005_alter_petimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='size',
            field=models.CharField(choices=[('miniatura', 'Miniatura'), ('pequeno', 'Pequeno'), ('médio', 'Médio'), ('grande', 'Grande')], editable=False, max_length=50),
        ),
    ]
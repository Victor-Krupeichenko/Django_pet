# Generated by Django 4.2.3 on 2023-07-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название'),
        ),
    ]
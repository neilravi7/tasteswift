# Generated by Django 4.2.4 on 2023-09-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='cuisine_type',
        ),
        migrations.AddField(
            model_name='vendor',
            name='cuisine_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]

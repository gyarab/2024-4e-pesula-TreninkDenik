# Generated by Django 5.1.6 on 2025-03-04 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_trenink_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="uzivatel",
            name="active",
            field=models.BooleanField(default=True),
        ),
    ]

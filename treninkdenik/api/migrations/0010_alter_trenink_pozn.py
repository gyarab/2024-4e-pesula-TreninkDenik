# Generated by Django 5.1.6 on 2025-03-23 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_alter_trenink_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trenink",
            name="pozn",
            field=models.TextField(max_length=200),
        ),
    ]

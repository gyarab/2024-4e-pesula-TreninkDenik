# Generated by Django 5.1.6 on 2025-03-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_remove_uzivatel_jmeno_alter_uzivatel_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uzivatel",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]

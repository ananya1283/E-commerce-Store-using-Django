# Generated by Django 5.1.7 on 2025-03-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="images/"),
        ),
    ]

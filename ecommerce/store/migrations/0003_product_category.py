# Generated by Django 5.1.7 on 2025-03-20 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="Category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="store.category",
            ),
        ),
    ]

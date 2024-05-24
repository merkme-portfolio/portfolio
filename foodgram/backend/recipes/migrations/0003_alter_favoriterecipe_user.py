# Generated by Django 4.2.6 on 2023-11-02 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favoriterecipe",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]

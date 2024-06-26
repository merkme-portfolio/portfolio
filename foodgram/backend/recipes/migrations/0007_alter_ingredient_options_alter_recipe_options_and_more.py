# Generated by Django 4.2.6 on 2023-11-03 09:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0006_alter_favoriterecipe_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "verbose_name": "Ingredient",
                "verbose_name_plural": "Ingredients",
            },
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "ordering": ("-pub_date",),
                "verbose_name": "Recipe",
                "verbose_name_plural": "Recipes",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags"},
        ),
    ]

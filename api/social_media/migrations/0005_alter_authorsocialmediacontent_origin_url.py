# Generated by Django 4.2.5 on 2024-02-03 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_media", "0004_alter_authorsocialmediacontent_main_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="origin_url",
            field=models.TextField(),
        ),
    ]

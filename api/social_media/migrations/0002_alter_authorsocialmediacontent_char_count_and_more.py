# Generated by Django 4.2.5 on 2024-02-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_media", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="char_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="creation_info_created_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="origin_unique_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="tag_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="token_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="unique_id",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="authorsocialmediacontent",
            name="unique_uuid",
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
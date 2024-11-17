# Generated by Django 5.1.1 on 2024-11-03 01:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twits', '0002_alter_like_unique_together_remove_like_twit_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='twit',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_twits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='twit',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='twit',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='twit',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
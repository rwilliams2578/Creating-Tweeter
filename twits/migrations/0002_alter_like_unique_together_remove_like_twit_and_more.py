# Generated by Django 5.1.1 on 2024-11-03 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twits', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='like',
            name='twit',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='twit',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='twit',
            name='body',
            field=models.TextField(help_text='Main content of the Twit'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]

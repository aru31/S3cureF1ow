# Generated by Django 2.1.1 on 2018-09-29 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identity',
            name='files',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]

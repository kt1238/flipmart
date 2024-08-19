# Generated by Django 5.0.7 on 2024-08-06 06:19

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0013_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='text',
            new_name='details',
        ),
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2010,10,1)),
            preserve_default=False,
        ),
    ]

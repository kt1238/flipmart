# Generated by Django 5.0.7 on 2024-07-26 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0004_remove_user_cart_cartitem_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='null.jpg', upload_to=''),
        ),
    ]

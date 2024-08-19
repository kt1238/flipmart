# Generated by Django 5.0.7 on 2024-07-25 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0003_cart_user_cart_delete_shoppingcart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cart',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteadmin.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]

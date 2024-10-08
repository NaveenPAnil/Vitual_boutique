# Generated by Django 5.0.6 on 2024-05-20 11:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('image', models.ImageField(upload_to='brand/')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
                'db_table': 'vendor_app_brand',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('no_of_items', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'db_table': 'vendor_app_cart',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('image', models.ImageField(upload_to='category/')),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.brand')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'vendor_app_category',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product/')),
                ('display_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'vendor_app_product',
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.product')),
            ],
            options={
                'verbose_name': 'product size',
                'verbose_name_plural': 'product sizes',
                'db_table': 'vendor_app_productsize',
            },
        ),
        migrations.CreateModel(
            name='ProductAlternative',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('display_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('stock', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.product')),
                ('sizes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.productsize')),
            ],
            options={
                'verbose_name': 'product alternative',
                'verbose_name_plural': 'product alternatives',
                'db_table': 'vendor_app_productalternative',
            },
        ),
    ]

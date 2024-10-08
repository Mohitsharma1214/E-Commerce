# Generated by Django 5.0.3 on 2024-04-24 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_size_sizes_size_name_remove_products_sizes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='sizes',
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='products',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='store.size'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-24 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_size_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]

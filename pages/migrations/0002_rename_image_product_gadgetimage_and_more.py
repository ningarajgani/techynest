# Generated by Django 5.0.6 on 2024-10-18 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='gadgetImage',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='gadget_name',
            new_name='gadgetName',
        ),
    ]

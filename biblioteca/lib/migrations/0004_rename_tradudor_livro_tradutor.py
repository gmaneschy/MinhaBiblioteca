# Generated by Django 5.2.1 on 2025-05-23 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0003_livro_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livro',
            old_name='tradudor',
            new_name='tradutor',
        ),
    ]

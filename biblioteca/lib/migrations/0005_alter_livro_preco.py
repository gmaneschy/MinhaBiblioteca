# Generated by Django 5.2.1 on 2025-05-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0004_rename_tradudor_livro_tradutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='preco',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Preço'),
        ),
    ]

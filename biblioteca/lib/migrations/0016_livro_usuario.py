# Generated by Django 5.2.1 on 2025-06-02 19:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0015_remove_livro_arquivo_anotacoes_alter_livro_anotacoes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='livros', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

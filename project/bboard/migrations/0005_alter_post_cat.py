# Generated by Django 4.2 on 2023-06-29 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_onetimecode_alter_post_cat_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cat',
            field=models.CharField(choices=[('Potion masters', 'Зельевары'), ('Damage dealers', 'ДД'), ('Blacksmiths', 'Кузнецы'), ('Tanks', 'Танки'), ('Guild masters', 'Гилдмастеры'), ('Spell masters', 'Мастера заклинаний'), ('Heals', 'Хилы'), ('Quest givers', 'Квестгиверы'), ('Dealers', 'Торговцы'), ('Leatherworkers', 'Кожевники')], max_length=22, verbose_name='Категория'),
        ),
    ]
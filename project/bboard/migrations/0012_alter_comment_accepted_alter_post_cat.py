# Generated by Django 4.2 on 2023-07-14 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0011_alter_comment_accepted_alter_post_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='accepted',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='cat',
            field=models.CharField(choices=[('Tanks', 'Танки'), ('Potion masters', 'Зельевары'), ('Spell masters', 'Мастера заклинаний'), ('Guild masters', 'Гилдмастеры'), ('Quest givers', 'Квестгиверы'), ('Heals', 'Хилы'), ('Damage dealers', 'ДД'), ('Leatherworkers', 'Кожевники'), ('Dealers', 'Торговцы'), ('Blacksmiths', 'Кузнецы')], max_length=22, verbose_name='Категория'),
        ),
    ]

# Generated by Django 2.0.9 on 2018-11-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abyssal_modules', '0007_mutator_source_fk_part_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduledogmaattribute',
            name='short_name',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
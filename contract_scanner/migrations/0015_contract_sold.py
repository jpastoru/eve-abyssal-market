# Generated by Django 2.1.3 on 2018-12-23 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_scanner', '0014_plexpricerecord_change_latest_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='sold',
            field=models.BooleanField(null=True),
        ),
    ]
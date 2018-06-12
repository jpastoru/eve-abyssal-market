# Generated by Django 2.0.5 on 2018-06-11 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abyssal_modules', '0004_creator'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Creator',
            new_name='EveCharacter',
        ),
        migrations.AlterField(
            model_name='module',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creations', to='abyssal_modules.EveCharacter'),
        ),
    ]
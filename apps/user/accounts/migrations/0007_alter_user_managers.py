# Generated by Django 3.2.17 on 2023-05-02 02:07

import apps.user.accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20230502_1105'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', apps.user.accounts.models.UserManager()),
            ],
        ),
    ]
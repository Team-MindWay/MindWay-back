# Generated by Django 3.2.17 on 2023-03-15 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_alter_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='student',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='team',
        ),
        migrations.DeleteModel(
            name='Library',
        ),
        migrations.DeleteModel(
            name='TeamMember',
        ),
    ]

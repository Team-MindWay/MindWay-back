# Generated by Django 3.2.17 on 2023-06-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0013_alter_recommend_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommend',
            name='category',
            field=models.CharField(choices=[('novel', 'novel'), ('essay', 'essay')], default=None, max_length=30, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HPApp', '0009_remove_user_groups_remove_user_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]

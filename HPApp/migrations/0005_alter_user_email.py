# Generated by Django 5.1.1 on 2024-10-27 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HPApp', '0004_remove_patient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]

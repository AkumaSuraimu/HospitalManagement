# Generated by Django 5.1.1 on 2024-11-07 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HPApp', '0014_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=511)),
                ('doctor', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='HPApp.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HPApp.patient')),
            ],
        ),
    ]

# Generated by Django 5.1.1 on 2024-12-02 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HPApp', '0019_alter_timeinandoutdoctor_time_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeinandoutstaff',
            name='time_out',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 5.1.7 on 2025-03-21 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_column_field_alter_project_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True, null=True),
        ),
    ]

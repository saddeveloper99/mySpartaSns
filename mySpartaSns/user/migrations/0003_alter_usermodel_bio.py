# Generated by Django 4.2 on 2023-04-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_usermodel_managers_remove_usermodel_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='bio',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
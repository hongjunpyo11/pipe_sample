# Generated by Django 4.1.7 on 2023-04-16 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0004_rename_scriptpermission_scriptuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='public_yn',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.0 on 2022-07-29 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_userstoragedata_notiftypes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstoragedata',
            name='notifTypes',
            field=models.JSONField(default=list),
        ),
    ]

# Generated by Django 4.0 on 2022-07-31 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_kanban_taskcolumns_notification_is_read_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanban',
            name='party',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.party'),
        ),
    ]

# Generated by Django 4.0 on 2022-07-31 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_task_taskcolumn_remove_tasks_column_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='archive_by',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_due',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='timeToArchive',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskcolumn',
            name='archive_by',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='taskcolumn',
            name='archived_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taskcolumn',
            name='state',
            field=models.CharField(default='active', max_length=256),
        ),
        migrations.AlterField(
            model_name='taskcolumn',
            name='trash_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
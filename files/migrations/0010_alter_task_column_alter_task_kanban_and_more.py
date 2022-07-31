# Generated by Django 4.0 on 2022-07-31 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0009_alter_task_archive_by_alter_task_date_due_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.taskcolumn'),
        ),
        migrations.AlterField(
            model_name='task',
            name='kanban',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.kanban'),
        ),
        migrations.AlterField(
            model_name='taskcolumn',
            name='kanban',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.kanban'),
        ),
    ]
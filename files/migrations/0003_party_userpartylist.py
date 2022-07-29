# Generated by Django 4.0 on 2022-07-29 18:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('files', '0002_rename_storage_max_kb_userstoragedata_storage_max_b_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('joinHow', models.CharField(default='invite', max_length=256)),
                ('codeHash', models.CharField(default='NULL', max_length=256)),
                ('codeSalt', models.CharField(default='NULL', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserPartyList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='member', max_length=256)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('party', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.party')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
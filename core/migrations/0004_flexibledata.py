# Generated by Django 3.1.3 on 2020-12-16 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_trialinstance'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexibleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=99999)),
                ('value', models.CharField(max_length=99999)),
            ],
        ),
    ]

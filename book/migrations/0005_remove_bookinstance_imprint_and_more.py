# Generated by Django 4.1.7 on 2023-04-23 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_bookinstance_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinstance',
            name='imprint',
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='due_back',
            field=models.DateField(default=datetime.datetime(2023, 4, 30, 12, 18, 23, 544116), help_text='Default one week (7days).'),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-18 05:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201217_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signed_up',
            field=models.DateField(default=datetime.date(2020, 12, 18)),
        ),
    ]

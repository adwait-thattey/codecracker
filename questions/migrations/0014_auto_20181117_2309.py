# Generated by Django 2.1.2 on 2018-11-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_auto_20181117_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='view_count',
            field=models.IntegerField(default=0, max_length=7, verbose_name='Question View Count'),
        ),
    ]

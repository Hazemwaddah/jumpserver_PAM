# Generated by Django 3.2.14 on 2022-12-02 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acls', '0007_auto_20221202_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandgroup',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Comment'),
        ),
    ]

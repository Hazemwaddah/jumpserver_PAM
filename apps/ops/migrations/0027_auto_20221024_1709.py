# Generated by Django 3.2.14 on 2022-12-05 03:23

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0112_gateway_to_asset'),
        ('ops', '0026_auto_20221009_2050'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTaskExecution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('args', models.JSONField(verbose_name='Args')),
                ('kwargs', models.JSONField(verbose_name='Kwargs')),
                ('state', models.CharField(max_length=16, verbose_name='State')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Finished')),
                ('date_published', models.DateTimeField(auto_now_add=True, verbose_name='Date published')),
                ('date_start', models.DateTimeField(null=True, verbose_name='Date start')),
                ('date_finished', models.DateTimeField(null=True, verbose_name='Date finished')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Updated by')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('org_id',
                 models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('is_periodic', models.BooleanField(default=False, verbose_name='Periodic perform')),
                ('interval', models.IntegerField(blank=True, default=24, null=True, verbose_name='Cycle perform')),
                ('crontab', models.CharField(blank=True, max_length=128, null=True, verbose_name='Regularly perform')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True, verbose_name='Name')),
                ('instant', models.BooleanField(default=False)),
                ('args', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Args')),
                ('module', models.CharField(choices=[('shell', 'Shell'), ('win_shell', 'Powershell')], default='shell',
                                            max_length=128, null=True, verbose_name='Module')),
                ('chdir', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Chdir')),
                ('timeout', models.IntegerField(default=60, verbose_name='Timeout (Seconds)')),
                ('type', models.CharField(choices=[('adhoc', 'Adhoc'), ('playbook', 'Playbook')], default='adhoc',
                                          max_length=128, verbose_name='Type')),
                ('runas', models.CharField(default='root', max_length=128, verbose_name='Runas')),
                ('runas_policy', models.CharField(
                    choices=[('privileged_only', 'Privileged Only'), ('privileged_first', 'Privileged First'),
                             ('skip', 'Skip')], default='skip', max_length=128, verbose_name='Runas policy')),
                ('use_parameter_define', models.BooleanField(default=False, verbose_name='Use Parameter Define')),
                ('parameters_define', models.JSONField(default=dict, verbose_name='Parameters define')),
                ('comment',
                 models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Comment')),
                ('assets', models.ManyToManyField(to='assets.Asset', verbose_name='Assets')),
                ('owner',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='Creator')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='JobExecution',
            fields=[
                ('created_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Created by')),
                ('updated_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='Updated by')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('org_id',
                 models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('task_id', models.UUIDField(null=True)),
                ('status', models.CharField(default='running', max_length=16, verbose_name='Status')),
                ('parameters', models.JSONField(default=dict, verbose_name='Parameters')),
                ('result', models.JSONField(blank=True, null=True, verbose_name='Result')),
                ('summary', models.JSONField(default=dict, verbose_name='Summary')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_start', models.DateTimeField(db_index=True, null=True, verbose_name='Date start')),
                ('date_finished', models.DateTimeField(null=True, verbose_name='Date finished')),
                ('creator',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='Creator')),
                ('job',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='executions',
                                   to='ops.job')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.RemoveField(
            model_name='playbookexecution',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='playbookexecution',
            name='task',
        ),
        migrations.AlterUniqueTogether(
            name='playbooktemplate',
            unique_together=None,
        ),
        migrations.AlterModelOptions(
            name='celerytask',
            options={'ordering': ('name',)},
        ),
        migrations.RenameField(
            model_name='adhoc',
            old_name='owner',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='celerytask',
            old_name='date_finished',
            new_name='last_published_time',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='account',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='account_policy',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='crontab',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='date_last_run',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='interval',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='is_periodic',
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='last_execution',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='args',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='is_finished',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='kwargs',
        ),
        migrations.RemoveField(
            model_name='celerytask',
            name='state',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='account',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='account_policy',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='crontab',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='date_last_run',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='interval',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='is_periodic',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='last_execution',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='template',
        ),
        migrations.AddField(
            model_name='adhoc',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='playbook',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='adhoc',
            name='module',
            field=models.CharField(choices=[('shell', 'Shell'), ('win_shell', 'Powershell')], default='shell',
                                   max_length=128, verbose_name='Module'),
        ),
        migrations.AlterField(
            model_name='celerytask',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='playbook',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='playbook',
            name='name',
            field=models.CharField(max_length=128, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='playbook',
            name='path',
            field=models.FileField(upload_to='playbooks/'),
        ),
        migrations.DeleteModel(
            name='AdHocExecution',
        ),
        migrations.DeleteModel(
            name='PlaybookExecution',
        ),
        migrations.DeleteModel(
            name='PlaybookTemplate',
        ),
        migrations.AddField(
            model_name='job',
            name='playbook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ops.playbook',
                                    verbose_name='Playbook'),
        ),
    ]

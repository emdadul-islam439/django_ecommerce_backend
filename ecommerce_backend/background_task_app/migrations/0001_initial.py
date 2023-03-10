# Generated by Django 4.1.5 on 2023-01-03 18:24

import background_task_app.enums
from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
        ('store_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSendingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('Active', 'Active'), ('Disabled', 'Disabled')], default=background_task_app.enums.SetupStatus['active'], enum_class=background_task_app.enums.SetupStatus, max_length=8)),
                ('time_interval', django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('1 min', '1 min'), ('5 mins', '5 mins'), ('1 hour', '1 hour')], default=background_task_app.enums.TimeInterval['five_mins'], enum_class=background_task_app.enums.TimeInterval, max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('immediate_email', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='immediate_email', to='django_celery_beat.periodictask')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='store_app.order')),
                ('scheduled_email', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_email', to='django_celery_beat.periodictask')),
            ],
            options={
                'verbose_name': 'EmailSendingTask',
                'verbose_name_plural': 'EmailSendingTasks',
            },
        ),
    ]

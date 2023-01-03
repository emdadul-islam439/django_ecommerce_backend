from django.contrib import admin
from background_task_app.models import EmailSendingTask

# Register your models here.
admin.site.register(EmailSendingTask)
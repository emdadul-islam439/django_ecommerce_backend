from django.urls import path

from .views import test_task


urlpatterns = [
    path('celery-test/', test_task, name='celery_test_url'),
    # TODO: add "send_order_completion_email", "send_registration_email", "send_order_cancellation_email" etc. urls
]
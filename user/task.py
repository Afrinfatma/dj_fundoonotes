from celery import shared_task
from time import sleep
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse


@shared_task #this is the decorator that will work for any app environment
def send_email_task(token,email_id):
    """
    sends mail if user registered using celery
    """
    send_mail(
        subject='User Registration using celery',
        message=settings.BASE_URL +
                reverse('verify_token', kwargs={"token": token}),
        from_email=None,
        recipient_list=email_id,
        fail_silently=False,
    )
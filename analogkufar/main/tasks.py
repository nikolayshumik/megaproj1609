from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(email):
    subject = 'Order Confirmation'
    message = 'Thank you for your order!'
    sender_email = 'nikolayshumik@gmail.com'

    send_mail(subject, message, sender_email, [email])
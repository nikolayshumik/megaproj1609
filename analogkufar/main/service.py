from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присыылать Вам много спама',
        'metelstas6@gmail.com',
        [user_email],
        fail_silently=False,
    )



from django.core.mail import send_mail
from .models import Mailing, Attempt

def send_mailing():
    mailings = Mailing.objects.filter(status='created')

    for mailing in mailings:
        clients = mailing.clients.all()
        message = mailing.message

        for client in clients:
            try:
                send_mail(
                    message.subject,
                    message.body,
                    'danieelpark@gmail.com',
                    [client.email],
                    fail_silently=False
                )
                Attempt.objects.create(mailing=mailing, status='success', server_response='Отправлено успешно')
            except Exception as e:
                Attempt.objects.create(mailing=mailing, status='failed', server_response=str(e))

from django.core.management.base import BaseCommand
from mailing.tasks import send_mailing


class Command(BaseCommand):
    help = 'Отправка всех запланированных рассылок'

    def handle(self, *args, **kwargs):
        send_mailing()
        self.stdout.write(self.style.SUCCESS('Успешная отправка всех рассылок'))

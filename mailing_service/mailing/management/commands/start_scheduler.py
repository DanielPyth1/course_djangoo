from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from mailing.tasks import send_mailing


class Command(BaseCommand):
    help = 'Запуск планировщика рассылок'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.add_job(send_mailing, 'interval', minutes=5, misfire_grace_time=300)
        self.stdout.write(self.style.SUCCESS('Планировщик запущен.'))

        scheduler.start()

        try:
            self.stdout.write(self.style.SUCCESS('Для завершения нажмите Ctrl+C.'))
            scheduler._thread.join()
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.WARNING('Планировщик остановлен.'))
            scheduler.shutdown()

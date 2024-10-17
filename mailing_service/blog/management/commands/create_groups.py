from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Создает группы Менеджер и Контент-менеджер'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа {manager_group.name} создана'))
            self.stdout.write(self.style.SUCCESS(f'Группа {content_manager_group.name} создана'))
        else:
            self.stdout.write(self.style.WARNING('Группы уже существуют'))

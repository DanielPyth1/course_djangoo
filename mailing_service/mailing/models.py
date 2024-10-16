from django.conf import settings
from django.db import models


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Mailing(models.Model):
    start_date = models.DateTimeField()
    frequency = models.CharField(max_length=50, choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'),
                                                         ('monthly', 'Раз в месяц')])
    status = models.CharField(max_length=50,
                              choices=[('created', 'Создана'), ('started', 'Запущена'), ('finished', 'Завершена')])
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('success', 'Успешно'), ('failed', 'Неуспешно')])
    server_response = models.TextField()

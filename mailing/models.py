from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(verbose_name='почта')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.', null=True, blank=True)
    comment = models.CharField(max_length=250, verbose_name='комментарий', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='владелец', null=True, blank=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        permissions = [
            ("disable_client", "Can disable client"),
        ]


class MailingMessage(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='владелец', null=True, blank=True)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'сообщение рассылки'
        verbose_name_plural = 'сообщения рассылок'


class MailingSettings(models.Model):
    PERIODS = [
        ('minute', 'раз в минуту'),
        ('hour', 'раз в часа'),
        ('day', 'раз в день'),
        ('week', 'раз в неделю'),
        ('month', 'раз в месяц'),
        ('year', 'раз в год'),
    ]

    STATUSES = [
        ('created', 'создана'),
        ('started', 'запущена'),
        ('completed', 'выполнена'),
        ('error', 'ошибка'),
    ]

    date_start_mailing = models.DateTimeField(verbose_name='дата начала рассылки', auto_now_add=True)
    date_next_mailing = models.DateTimeField(verbose_name="дата следующей рассылки", null=True, blank=True)
    date_end_mailing = models.DateTimeField(verbose_name='дата окончания рассылки', null=True, blank=True)
    periodicity_mailing = models.CharField(max_length=6, choices=PERIODS, default='minute', verbose_name='периодичность')
    mailing_status = models.CharField(max_length=15, choices=STATUSES, default='created', verbose_name='статус')
    clients = models.ManyToManyField(Client, verbose_name='Кому (клиенты сервиса)')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name="Сообщение", null=True)
    is_active = models.BooleanField(default=True, verbose_name='активация рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='владелец', null=True, blank=True)

    def __str__(self):
        return f'{self.periodicity_mailing} - {self.mailing_status}'

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылки'
        permissions = [
            ("disable_mailing", "Can disable mailing"),
        ]


class MailingTry(models.Model):
    datetime_try_last = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    try_status = models.BooleanField(default=False, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ сервера', null=True, blank=True)
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент', null=True, blank=True)

    def __str__(self):
        return f'{self.datetime_try_last} - {self.try_status}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'

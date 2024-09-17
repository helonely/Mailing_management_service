from datetime import datetime, timedelta

import pytz
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

from blog.models import Blog
from mailing.models import MailingSettings, MailingTry, Client


def get_blog_from_cache():
    if not settings.CACHE_ENABLED:
        return Blog.objects.all()
    key = "blog_list"
    blog = cache.get(key)
    if blog is not None:
        return blog
    blog = Blog.objects.all()
    cache.set(key, blog)
    return blog


def get_clients_count_from_cache():
    if not settings.CACHE_ENABLED:
        return Client.objects.all().values('email').distinct().count()
    key = "unique_clients_count"
    unique_clients_count = cache.get(key)
    if unique_clients_count is not None:
        return unique_clients_count
    unique_clients_count = Client.objects.all().values('email').distinct().count()
    cache.set(key, unique_clients_count)
    return unique_clients_count


def get_all_mailings_count_from_cache():
    if not settings.CACHE_ENABLED:
        return MailingSettings.objects.all().count()
    key = "active_mailings_count"
    all_mailings_count = cache.get(key)
    if all_mailings_count is not None:
        return all_mailings_count
    all_mailings_count = MailingSettings.objects.all().count()
    cache.set(key, all_mailings_count)
    return all_mailings_count


def get_active_mailings_count_from_cache():
    if not settings.CACHE_ENABLED:
        return MailingSettings.objects.all().filter(is_active=True).count()
    key = "active_mailings_count"
    active_mailings_count = cache.get(key)
    if active_mailings_count is not None:
        return active_mailings_count
    active_mailings_count = MailingSettings.objects.all().filter(is_active=True).count()
    cache.set(key, active_mailings_count)
    return active_mailings_count


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)

    # Получаем все рассылки
    mailings = MailingSettings.objects.filter(
        date_next_mailing__lte=current_time,
        mailing_status__in=['created', 'started']
    )

    # Обрабатываем каждую рассылку по отдельности
    for mailing in mailings:
        mailing.mailing_status = 'started'
        if mailing.date_end_mailing and current_time >= mailing.date_end_mailing:
            mailing.mailing_status = 'completed'
            mailing.save()  # Сохраняем статус перед началом обработки
            continue

        # Обрабатываем каждого клиента рассылки
        for client in mailing.clients.all():

            try:
                response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                MailingTry.objects.create(
                    mailing=mailing,
                    client=client,
                    try_status=True,
                    server_response=response,
                )

                print(f"Успешно отправлено письмо для {client.email}")
            except Exception as e:
                MailingTry.objects.create(
                    mailing=mailing,
                    client=client,
                    try_status=False,
                    server_response=str(e)
                )
                print(f"Не удалось отправить письмо для {client.email}: {str(e)}")

        # Обновляем дату следующей рассылки
        if mailing.periodicity_mailing == 'minute':
            mailing.date_next_mailing += timedelta(minutes=1)
        elif mailing.periodicity_mailing == 'hour':
            mailing.date_next_mailing += timedelta(hours=1)
        elif mailing.periodicity_mailing == 'day':
            mailing.date_next_mailing += timedelta(days=1)
        elif mailing.periodicity_mailing == 'week':
            mailing.date_next_mailing += timedelta(weeks=1)
        elif mailing.periodicity_mailing == 'month':
            mailing.date_next_mailing += timedelta(days=30)
        elif mailing.periodicity_mailing == 'year':
            mailing.date_next_mailing += timedelta(days=365)

        mailing.save()

    # После обработки всех рассылок, устанавливаем статус 'completed'
    mailings.update(mailing_status='completed')

    print("Все рассылки успешно обработаны.")

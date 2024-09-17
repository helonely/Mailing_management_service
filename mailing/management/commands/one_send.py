from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from mailing.models import MailingSettings, MailingTry
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings = MailingSettings.objects.filter(
            mailing_status__in=['started']
        )
        for mailing in mailings:
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



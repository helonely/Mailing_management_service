from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

from mailing.services import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler()  # Create a scheduler
        scheduler.add_job(func=send_mailing, trigger="interval", seconds=60)  # Add a job
        scheduler.start()  # Start the scheduler

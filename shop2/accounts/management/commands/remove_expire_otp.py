from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "remove all expire otp codes"

    def handle(self, *args, **options):
        now = timezone.now()
        expired_time = now - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt = expired_time).delete()
        self.stdout.write("all expired codes removed")
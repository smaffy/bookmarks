from django.core.management.base import BaseCommand, CommandError
from account.models import User
from datetime import datetime, timedelta


class Command(BaseCommand):
    """
    Delete inactive users after 30 days without login'
    """

    def handle(self, *args, **options):
        past_date = datetime.now() - timedelta(days=30)
        User.objects.filter(is_active=True, last_login__lte=past_date).delete()

        self.stdout.write('Deleted users inactive and did not login 30 days')
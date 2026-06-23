from django.core.management.base import BaseCommand
from reservations.services import expirer_reservations


class Command(BaseCommand):
    help = "Expire les réservations ayant dépassé le délai configuré."

    def handle(self, *args, **options):
        total = expirer_reservations()
        self.stdout.write(self.style.SUCCESS(f"{total} réservation(s) expirée(s)."))


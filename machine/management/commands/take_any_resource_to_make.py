from django.core.management.base import BaseCommand

from machine.models import Machine


class Command(BaseCommand):
    help = 'Take any resource to make it'

    def handle(self, *args, **options):
        machine = Machine.objects.filter(serial_port__null=False).first()

        if not machine.external_fabric_id:
            ...

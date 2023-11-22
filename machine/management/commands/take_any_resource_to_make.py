import syapi
from django.conf import settings
from django.core.management.base import BaseCommand

from machine.models import Machine, Resource


def start_making_resource(machine, resource):
    success_started = True
    return success_started


class Command(BaseCommand):
    help = 'Take any resource to make it'

    def handle(self, *args, **options):
        url_resource = settings.MICROSERVICES_URLS['resource']
        api_resource = syapi.Resource(token=settings.USER_TOKENS['resource'], url=url_resource)
        api_fabric = syapi.Fabric(token=settings.USER_TOKENS['resource'], url=url_resource)

        machines = Machine.objects.filter(serial_port__null=False, work_status=Machine.WORK_STATUS_READY_TO_MAKE)
        for machine in machines:
            if not machine.external_fabric_id:
                external_fabric_data = api_fabric.create(title=machine.title)
                machine.external_fabric_id = external_fabric_data['id']
                machine.save()

            external_resource_data = api_resource.take_any_to_make(fabric_id=machine.external_fabric_id)
            resource = Resource(machine=machine, external_resource_id=external_resource_data['id'])
            success_started = start_making_resource(machine, resource)
            if not success_started:
                resource.making_status = Resource.MAKING_STATUS_CANCEL
                # TODO: залогировать причину незапуска изготовления ресурса
                # TODO: послать микросервису ресурсов запрос об отмене изготовления, передав причину

            resource.save()

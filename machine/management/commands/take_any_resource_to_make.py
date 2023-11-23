import serial
import syapi
from django.conf import settings
from django.core.management.base import BaseCommand

from machine.models import Machine, Resource, BAUDRATES


def guess_baudrate(machine):
    gcode = 'G0 X0\n'.encode()
    success_answer = 'ok\n'.encode()
    for baudrate_to_check in BAUDRATES[10:27]:
        with serial.Serial(
                machine.serial_port,
                baudrate=baudrate_to_check,
                timeout=0.1,
                write_timeout=0.1,
        ) as opened_serial:
            opened_serial.write(gcode)
            answer = opened_serial.read(100)
            if answer.endswith(success_answer):
                return baudrate_to_check


def start_making_resource(machine: Machine, resource: Resource):
    success_started = True
    with serial.Serial(
            machine.serial_port,
            baudrate=machine.port_baudrate,
            timeout=machine.port_read_timeout,
            write_timeout=machine.port_write_timeout,
    ) as opened_serial:
        opened_serial.write('G0 X10 Y10 Z10\n'.encode())
        print(opened_serial.read(100))

    return success_started


class Command(BaseCommand):
    help = 'Take any resource to make it'

    def handle(self, *args, **options):
        url_resource = settings.MICROSERVICES_URLS['resource']
        api_resource = syapi.Resource(token=settings.USER_TOKENS['resource'], url=url_resource)
        api_fabric = syapi.Fabric(token=settings.USER_TOKENS['resource'], url=url_resource)

        machines = Machine.objects.filter(serial_port__isnull=False, work_status=Machine.WORK_STATUS_READY_TO_MAKE)
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

            # resource.save()

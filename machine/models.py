from django.db import models
from serial.tools.list_ports import comports


# class MachineType(models.Model):
#     title = models.CharField('Название типа', max_length=25)
#     technology_type = models.IntegerField('Тип технологии производства (аддитивная, сабстрактивая, смешанная, манпуляция)')


def get_serial_ports():
    comport_choices = []
    for port, desc, hwid in comports():
        device_name = desc
        comport_choices.append([port, device_name])

    return comport_choices


class Machine(models.Model):
    WORK_STATUS_READY_TO_MAKE = 1
    WORK_STATUS_BUSY = 2
    WORK_STATUS_REPAIR = 3
    WORK_STATUS_CHOICES = (
        (WORK_STATUS_READY_TO_MAKE, 'Готов к работе'),
        (WORK_STATUS_BUSY, 'Занят'),
        (WORK_STATUS_REPAIR, 'На тех. обслуживании'),
    )
    work_status = models.IntegerField('Статус станка', choices=WORK_STATUS_CHOICES, default=WORK_STATUS_READY_TO_MAKE)
    title = models.CharField('Название станка', max_length=250)
    external_fabric_id = models.IntegerField('Идентификатор машины как фабрики', null=True)
    # machine_type = models.ForeignKey(MachineType)
    serial_port = models.CharField('Последовательный порт', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Станок'
        verbose_name_plural = 'Станки'


class Resource(models.Model):
    MAKING_STATUS_MAKING = 1
    MAKING_STATUS_MADE = 2
    MAKING_STATUS_CANCEL = 3
    MAKING_STATUS_CHOICES = (
        (MAKING_STATUS_MAKING, 'В процессе изготовления'),
        (MAKING_STATUS_MADE, 'Изготовлен'),
        (MAKING_STATUS_CANCEL, 'Изготовление отменено'),
    )
    external_title = models.CharField('Название ресурса', max_length=250)
    making_status = models.IntegerField('Статус ресурса', choices=MAKING_STATUS_CHOICES, default=MAKING_STATUS_MAKING)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='resources')
    external_resource_id = models.IntegerField('Идентификатор ресурса из микросервиса')

    def __str__(self):
        return self.external_title

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

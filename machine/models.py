from django.db import models


# class MachineType(models.Model):
#     title = models.CharField('Название типа', max_length=25)
#     technology_type = models.IntegerField('Тип технологии производства (аддитивная, сабстрактивая, смешанная, манпуляция)')


class Machine(models.Model):
    title = models.CharField('Название станка', max_length=250)
    external_fabric_id = models.IntegerField('Идентификатор машины как фабрики', null=True)
    # machine_type = models.ForeignKey(MachineType)
    serial_port = models.CharField('Последовательный порт', max_length=50)

    class Meta:
        verbose_name = 'Станок'
        verbose_name_plural = 'Станки'

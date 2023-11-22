from django.contrib import admin

from machine.models import Machine


class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'serial_port', 'external_fabric_id')
    readonly_fields = ('external_fabric_id',)


admin.site.register(Machine, MachineAdmin)

from django.contrib import admin
from django.forms import ModelForm, Select

from machine.models import Machine, Resource, get_serial_ports


class MachineAdminForm(ModelForm):
    class Meta:
        widgets = {'serial_port': Select(choices=get_serial_ports())}


class MachineAdmin(admin.ModelAdmin):
    form = MachineAdminForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.form.Meta.widgets['serial_port'] = Select(choices=get_serial_ports())
        return super().get_form(*args, **kwargs)

    list_display = ('id', 'title', 'serial_port', 'external_fabric_id')
    readonly_fields = ('external_fabric_id',)


admin.site.register(Machine, MachineAdmin)


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'making_status', 'external_resource_id', 'external_title')
    readonly_fields = ('external_title', 'external_resource_id')


admin.site.register(Resource, ResourceAdmin)

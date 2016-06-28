from django.contrib import admin

from pipelines.models import Pipeline


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]
    list_display = [
        'name',
    ]

    def has_delete_permission(self, request, obj=None):
        return False

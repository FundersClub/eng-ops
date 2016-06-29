from django.contrib import admin

from pipelines.models import (
    Pipeline,
    PipelineState,
)


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


@admin.register(PipelineState)
class PipelineStateAdmin(admin.ModelAdmin):
    fields = [
        'started_at',
        'issue',
        'pipeline',
        'ended_at',
    ]
    list_display = [
        'started_at',
        'issue',
        'pipeline',
        'ended_at',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
